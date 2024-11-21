import * as utils from '../../geral/js/utils.js';
import { ConfirmationModal } from '../../geral/js/modals.js';
import { PackageGrid } from '../../geral/js/packageGrid.js';
import { Form } from './form.js';
import {AutoComplete} from './autoComplete.js';


// Função construtora do formulário
export class FormINJ extends Form{
    constructor() {
        super()
        this.fields.codmol = this.form.querySelector('#codmolde')
        this.fields.codori.isScope = codori => ['INJ', 'HAB'].includes(codori)
        this.fields.codetg.isScope = codetg => [1500, 8000].includes(this.getIdValue(codetg))
        this.fields.codori.autoComplete.setFiltersDB({codori__in:['INJ', 'HAB']})
        this.fields.codpro.autoComplete.setFiltersDB({codori__in:['INJ', 'HAB']})
        this.packageGrid = new PackageGrid()
        this.URL = '/apontamento/injecao' 
        //--------------------Eventos-------------------------
        // Adição de embalagens
        this.btAddPackage.addEventListener('click', e => 
            this.opSelected ? this.packageGrid.addPackage() : utils.setMessage('Selecione uma Ordem de Produção!', 'error', this.lbMessage))
        
        // Apontamento 
        this.btToProdReporting.addEventListener('click', async e => {
            if(e.target.value === 'A') this.validateForm()
            else if (e.target.value === 'I') this.printTag()
        })
        // cancelar
        this.btCancel.addEventListener('click', this.checkCancel)
    }

      // Definição de campos conforme O.P, sobrescrição
    setFieldsOP = (OP) => {
        this.setFieldsOPSuper(OP)
        this.packageGrid.deposito.coddep = OP.coddep
        this.packageGrid.deposito.desdep = OP.desdep
        this.packageGrid.dataNum = OP.datatu
        this.packageGrid.produto = OP.codpro
        this.fields.codmol.autoComplete = new AutoComplete(this.fields.codmol, this.script_production)
        this.fields.codmol.autoComplete.setFiltersDB({codpro:OP.codpro})
    }

    // remove todos os campos baseados em OP
    cancel = () => {
        utils.clearInputs(Object.values(this.fields))
        utils.enableInputs([this.fields.codori, this.fields.codpro])
        this.packageGrid.clear()
        utils.clearMessage(this.lbMessage)
        utils.clearMessage(this.lbMessageOp)
        this.script_production.length = 0
        this.opSelected = false
        this.fields.codmol.autoComplete = null
        this.packageGrid.deposito.coddep = null
        this.packageGrid.deposito.desdep = null
        this.packageGrid.produto = null
        this.packageGrid.dataNum = null
        this.btToProdReporting.value = "A"
        this.btToProdReporting.textContent = "Apontar"  
        this.prodReportingMade = false
        this.btAddPackage.removeAttribute('disabled')
    }

    // verifica situação antes de cancelar
    checkCancel = () => {
        let extraMessage = ''
        let notPrinted = this.packageGrid.packages.filter(packageItem => packageItem.created && !packageItem.printed).length
        if (notPrinted > 0) 
            extraMessage = `<br><span class="text-red-500">Atenção! existem ${notPrinted} embalagem(s) criada(s) porém pendente(s) de impressão!</span>`
        else if (this.prodReportingMade && notPrinted === 0) {
            this.cancel()
            return
        }
        new ConfirmationModal(
            'Cancelamento',
            `Você tem certeza que  deseja cancelar este apontamento? ${extraMessage}`,
            this.cancel 
        )
    }
    
     // valida embalagens
     validatePackages = () => {
        let packagesQtd = this.packageGrid.packages.map(packageItem => packageItem.inpQtdEmb)
        utils.validateInputs(packagesQtd)
        if (packagesQtd.length === 0) {
            utils.setMessage('É necessário adicionar pelo menos uma embalagem!', 'error', this.lbMessage)
            return false
        }  
        let packagesInvalids = packagesQtd.filter(packageQtd => !(parseInt(packageQtd.value) > 0))      
        if (packagesInvalids.length > 0) {
            utils.invalidateInputs(packagesInvalids)
            utils.setMessage('Existem embalagens sem quantidade definida ou inválida!', 'error', this.lbMessage)
            return false
        }
        return true 
    } 

    // Calcula total do apontamento
    getFullQtdReport = () => this.packageGrid.sumarizePackages()

    // apontar
    ToProdReporting = async () => {
        utils.isLoading(this.loading, true)
        // Montagem do payload
        let [datini, horini] = this.fields.inimov.value.split("T"); 
        let [datrea, horrea] = this.fields.fimmov.value.split("T"); 
        let request = {
            codori:this.fields.codori.value,
            numorp:this.fields.numorp.value,
            codetg:this.getIdValue(this.fields.codetg.value),
            seqrot:this.getIdValue(this.fields.seqrot.value),
            codpro: this.fields.codpro.value,
            datini: datini.split("-").reverse().join("/"),
            horini: horini,
            datrea: datrea.split("-").reverse().join("/"),
            horrea: horrea,
            numcad:this.getIdValue(this.fields.numcad.value),
            codcre:this.fields.codcre.value,
            codmol:this.fields.codmol.value,
            embalagens: []
        }
        this.packageGrid.packages.forEach(packageItem => request.embalagens.push({
            codpro: packageItem.codpro,
            coddep: packageItem.deposito.coddep,
            qtdemb: parseInt(packageItem.inpQtdEmb.value) || 0
        }))
        // envio da requisição
        try { 
            let response = await utils.ajaxRequest(this.URL, request) 
            if (response.erro) utils.setMessage(response.retorno, "error", this.lbMessage)
            else this.setProdReporting(response)
        }
        catch (error) { 
            utils.setMessage('Ocorreu um erro ao tentar se comunicar com o servidor!', 'error', this.lbMessage) 
        }
        utils.isLoading(this.loading, false); 
    }

    // definições pos apontamento com sucesso
    setProdReporting = (prodReporting) => {
        utils.setMessage(prodReporting.retorno, "success", this.lbMessage) 
        for (let i in prodReporting.embalagens) 
            this.packageGrid.packages[i].confirmPackage(prodReporting.embalagens[i])

        this.btToProdReporting.value = "I"
        this.btToProdReporting.textContent = "Imprimir" 
        this.prodReportingMade = true  
        this.btCancel.textContent = "Limpar"
        this.btAddPackage.setAttribute('disabled', true)
    }

     // imprime etiquetas
     printTag = async () => {
        utils.clearMessage(this.lbMessage)
        utils.isLoading(this.loading, true)
        try {
            let response = await this.packageGrid.printTags(this.getIdValue(this.fields.codetg.value))
            let type =  response.error ? 'error' : 'succes'
            utils.setMessage(response.message, type, this.lbMessage)
        } catch {
            utils.setMessage("Ocorreu um erro ao tentar se comunicar com a impressora!", "error", this.lbMessage)
        }
        utils.isLoading(this.loading, false)
    }

}


document.addEventListener('DOMContentLoaded', () =>{ 
    const formInj = new FormINJ()
    window.addEventListener('beforeunload', e => {
        let notPrinted = formInj.packageGrid.packages.filter(packageItem => packageItem.created && !packageItem.printed).length
        if (notPrinted.length > 0) e.preventDefault() 
    })
})
