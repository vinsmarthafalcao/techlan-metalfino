import * as utils from '../../geral/js/utils.js';
import { QRCodeModal, ConfirmationModal } from '../../geral/js/modals.js';
import { ReportGrid } from './ReportGrid.js';
import { Form } from './form.js';

// Função construtora do formulário
export class FormGERAL extends Form{
    constructor() {
        super()
        this.reportGrid = new ReportGrid()
        this.qrCodeModal = new QRCodeModal(this.reportGrid.packagesExists, this.reportGrid.getPackage)
        this.URL = '/apontamento/geral' 
        this.fields.codori.isScope = codori => !['INJ'].includes(codori)
        this.fields.codetg.isScope = codetg => ![1500, 8000].includes(this.getIdValue(codetg))
        this.fields.codpro.autoComplete.setExcludesDB({codori__in:['INJ', 'HAB']})
        this.fields.codori.autoComplete.setExcludesDB({codori__in:['INJ', 'HAB']})
        //--------------------Eventos-------------------------
        // Adição de embalagens
        this.btAddPackage.addEventListener('click', e => 
            this.opSelected ? this.qrCodeModal.open() : utils.setMessage('Selecione uma Ordem de Produção!', 'error', this.lbMessage))
        
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
        this.reportGrid.setOP(OP)
    }

    // remove todos os campos baseados em OP
    cancel = () => {
        utils.clearInputs(Object.values(this.fields))
        utils.enableInputs([this.fields.codori, this.fields.codpro])
        this.reportGrid.clear()
        utils.clearMessage(this.lbMessage)
        utils.clearMessage(this.lbMessageOp)
        this.script_production.length = 0
        this.opSelected = false
        this.reportGrid.OP = null
        this.reportGrid.lote = null
        this.btToProdReporting.value = "A"
        this.btToProdReporting.textContent = "Apontar"  
        this.prodReportingMade = false
        this.btAddPackage.removeAttribute('disabled')
    }

    // verifica situação antes de cancelar
    checkCancel = () => {
        let extraMessage = ''
        let notPrinted = this.reportGrid.cardsReport.filter(card => card.created && !card.printed).length
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
            codlot: this.reportGrid.lote,
            datini: datini.split("-").reverse().join("/"),
            horini: horini,
            datrea: datrea.split("-").reverse().join("/"),
            horrea: horrea,
            numcad:this.getIdValue(this.fields.numcad.value),
            codcre:this.fields.codcre.value,
            embalagens: []
        }
        this.reportGrid.cardsReport.forEach(card => request.embalagens.push({
            numemb: card.packageRead.numemb,
            veremb: card.packageRead.veremb,
            codpro: card.codpro,
            coddep: card.deposito.coddep,
            proportion: card.packageRead.proportion,
            qtdemb: parseInt(card.ipQtd1Qld.value),
            qtdrfg: parseInt(card.ipQtdRfg.value)
        }))
        // envio da requisição
        console.log(request)
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
            this.reportGrid.cardsReport[i].confirmPackage(prodReporting.embalagens[i])

        this.btToProdReporting.value = "I"
        this.btToProdReporting.textContent = "Imprimir" 
        this.prodReportingMade = true  
        this.btCancel.textContent = "Limpar"
        this.btAddPackage.setAttribute('disabled', true)
    }

     // valida embalagens
     validatePackages = () => {
        let isValid = true
        if (this.reportGrid.cardsReport.length === 0) {
            utils.setMessage('É necessário ler pelo menos uma embalagem!', 'error', this.lbMessage)
            return false
        }  
        this.reportGrid.cardsReport.forEach(card => {
            utils.validateInputs([card.ipQtd1Qld, card.ipQtdRfg, card.ipBalance])
            if (!parseInt(card.ipQtd1Qld.value) > 0) {
                utils.invalidateInputs([card.ipQtd1Qld])
                utils.setMessage('Existem embalagens sem quantidades definidas ou inválidas!', 'error', this.lbMessage)
                isValid = false
            }
            if ((parseInt(card.ipQtd1Qld.value)+parseInt(card.ipQtdRfg.value))*card.packageRead.proportion+parseInt(card.ipBalance.value)!==card.packageRead.qtdemb){
                utils.invalidateInputs([card.ipQtd1Qld, card.ipQtdRfg, card.ipBalance])
                utils.setMessage('Existem embalagens com quantidades inconsistentes!', 'error', this.lbMessage)
                isValid = false
            }
            if (parseInt(card.ipBalance.value) < 0){
                utils.invalidateInputs([card.ipQtd1Qld, card.ipQtdRfg, card.ipBalance])
                utils.setMessage('A quantidade apontada + refugada não pode ser maior que a quantidade da embalagem lida!', 'error', this.lbMessage)
                isValid = false
            }
        })
        return isValid 
    } 

     // imprime etiquetas
     printTag = async () => {
        utils.clearMessage(this.lbMessage)
        utils.isLoading(this.loading, true)
        try {
            let response = await this.reportGrid.printTags(this.getIdValue(this.fields.codetg.value))
            let type =  response.error ? 'error' : 'succes'
            utils.setMessage(response.message, type, this.lbMessage)
        } catch {
            utils.setMessage("Ocorreu um erro ao tentar se comunicar com a impressora!", "error", this.lbMessage)
        }
        utils.isLoading(this.loading, false)
    }

    // Calcula total do apontamento
    getFullQtdReport = () => this.reportGrid.sumarizeReports()

}


document.addEventListener('DOMContentLoaded', () =>{ 
    const formGeral = new FormGERAL()
    window.addEventListener('beforeunload', e => {
        let notPrinted = formGeral.reportGrid.cardsReport.filter(card => card.created && !card.printed).length
        if (notPrinted.length > 0) e.preventDefault() 
    })
})
