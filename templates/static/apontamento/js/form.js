import {AutoComplete} from './autoComplete.js';
import * as utils from '../../geral/js/utils.js';
import { ConfirmationModal } from '../../geral/js/modals.js';

// Função construtora do formulário
export class Form{
    constructor () {
        //--------------------COMPONENTES--------------------------------
        this.form = document.getElementById('formApontamento')
        this.script_production = []
        this.fields = {
            codori: this.form.querySelector('#codori'),
            numorp: this.form.querySelector('#numorp'),
            codpro: this.form.querySelector('#codpro'),
            numcad: this.form.querySelector('#numcad'),
            inimov: this.form.querySelector('#inimov'),
            fimmov: this.form.querySelector('#fimmov'),
            codetg: this.form.querySelector('#codetg'),
            seqrot: this.form.querySelector('#seqrot'),
            codcre: this.form.querySelector('#codcre')
        }
        this.fields.codori.keyField = true
        this.fields.codori.isScope = codori => true
        this.fields.numorp.keyField = true
        this.fields.numorp.btSearch = this.form.querySelector('#openModalOp')
        this.fields.codetg.isScope = codetg => true
        this.opURL = this.fields.numorp.dataset.url
        this.URL = ''
        this.opSelected = false
        this.opModal = new OpModal(this)
        this.opLoading = this.form.querySelector('#opLoading')
        this.loading = this.form.querySelector('#grLoading')
        this.lbMessageOp = this.form.querySelector('#msgOp')
        this.lbMessage = this.form.querySelector('#msgGeral')
        this.btAddPackage = this.form.querySelector('#btAddEmb')
        this.btToProdReporting = this.form.querySelector('#btapontar')
        this.btCancel = this.form.querySelector('#btcancelar')
        this.prodReportingMade = false

        //--------------------EVENTOS----------------------------------
        // auto complete
        Object.values(this.fields).forEach(field => {
            if (field.classList.contains('autoComplete')) field.autoComplete = new AutoComplete(field, this.script_production)
        })
        // modal para seleção de OP
        this.fields.numorp.btSearch.addEventListener('click', e => this.opModal.open())
        // define origem baseado no produto
        this.fields.codpro.addEventListener('blur', () => setTimeout(() => 
            this.fields.codori.value = this.fields.codpro.autoComplete.option?.codori || '', 200))
        // remove produto se origem incondizente
        this.fields.codori.addEventListener('blur', e => {
            if (e.target.value !== this.fields.codpro.autoComplete.codori) this.fields.codpro.value = ''
            this.validateOP()
        })
        // validação da OP selecionada
        this.fields.numorp.addEventListener('blur', this.validateOP)

    }


    // valida ordem de produção selecionada
    validateOP = async () => {
        utils.isLoading(this.opLoading, true);
        const { codori, numorp } = this.fields;
        const keys = [ codori, numorp ]
        utils.validateInputs(keys);
        utils.clearMessage(this.lbMessageOp); 

        if (!numorp.value) { 
            utils.enableInputs([codori, this.fields.codpro])
            utils.isLoading(this.opLoading, false); 
            return; 
        }
        if (!codori.value) {
            utils.setMessage("É Obrigatório selecionar uma Origem!", "error", this.lbMessageOp);
            utils.invalidateInputs(keys);
            utils.isLoading(this.opLoading, false);
            return; 
        }
        if(!codori.isScope(codori.value)) {
            utils.setMessage(`Origem ${codori.value} não está na abrangência desta interface!`, "error", this.lbMessageOp);
            utils.invalidateInputs(keys);
            utils.isLoading(this.opLoading, false);
            return; 
        }
        const request = { codori: codori.value, numorp: numorp.value };
        try { 
            const validOP = await utils.ajaxRequest(this.opURL, request); 
            if (!validOP) {
                utils.invalidateInputs(keys);
                utils.setMessage("A Ordem de Produção selecionada é inválida ou não está ativa!", "error", this.lbMessageOp);
            } else this.setFieldsOP(validOP)
        }
        catch { 
            utils.setMessage("Ocorreu um erro ao tentar se comunicar com o servidor!", "error", this.lbMessageOp);
         }
        
        utils.isLoading(this.opLoading, false); 
    }

    // define campos conforme OP selecionada
    setFieldsOPSuper = (OP) => {
        this.setDates(OP.datatu)
        this.fields.codori.value = OP.codori
        this.fields.codpro.value = OP.codpro
        this.fields.numorp.value = OP.numorp
        this.fields.numcad.value = OP.numcad
        this.script_production.length = 0
        this.script_production.push(...OP.roteiro.filter(step => this.fields.codetg.isScope(step.codetg)))
        this.fields.codetg.value = this.script_production[0].codetg
        this.fields.seqrot.value = this.script_production[0].seqrot
        this.fields.codcre.value = this.script_production[0].codcre
        this.opSelected = true
        utils.disableInputs([this.fields.codori, this.fields.codpro])  
        this.fields.codcre.autoComplete.setFilters({codetg: this.script_production.map(script => this.getIdValue(script.codetg))})   
    }

    // define datas do formulário baseado na data atual
    setDates = currentDate => {
        currentDate = 
        this.fields.inimov.value = currentDate.substring(0, currentDate.length - 2) + '00'
        this.fields.fimmov.value = currentDate.substring(0, currentDate.length - 2) + '30'
    } 

    // validação do formulário
    validateForm = () => {
        utils.clearMessage(this.lbMessage)
        if (this.validateRequireds() && this.validateDates() && this.validatePackages() && this.validateScope()){
            new ConfirmationModal(
                `Apontamento de Produção`, 
                `Confirma o apontamento de ${this.getFullQtdReport()} unidade(s) do produto 
                ${this.fields.codpro.value} na Ordem de Produção ${this.fields.codori.value}-${this.fields.numorp.value}?`,
                this.ToProdReporting
            )
        }
    }

    // validação de campos obirgatórios
    validateRequireds = () => {
        let  [fields, isValid] = [Object.values(this.fields), true]
        utils.validateInputs(fields)

        if (!this.opSelected){
            utils.invalidateInputs([this.fields.codori, this.fields.numorp])
            utils.setMessage('Selecione uma Ordem de Produção!', 'error', this.lbMessage)
            return false
        }
        fields.forEach(field => {
            if (field.classList.contains('required') &&  field.value === ''){
                isValid = false
                utils.invalidateInputs([field])
            }
        })
        if  (!isValid) utils.setMessage('Campos obrigatórios não foram preenchidos!', 'error', this.lbMessage)
        return isValid
    }

    // Valida abrangência
    validateScope = () => {
        let isValid = true
        Object.values(this.fields).forEach(field => {
            if (field.isScope && !field.isScope(field.value)){
                isValid = false
                utils.invalidateInputs([field])
            }
        })
        if  (!isValid) utils.setMessage('Os valores nos campos indicados não estão na abrangência da interface!', 'error', this.lbMessage)
        return isValid
    }

    // validação de datas
    validateDates = () => {
        let isValid = false
        let inimov = new Date(this.fields.inimov.value) 
        let fimmov = new Date(this.fields.fimmov.value) 
        if (!inimov || !fimmov) utils.setMessage('Obrigatório selecionar o inicio e fim do movimento!', 'error', this.lbMessage)
        else if (inimov > fimmov) utils.setMessage('Inicio do movimento não pode ser maior que o fim!', 'error', this.lbMessage)
        else if (inimov.toISOString() === fimmov.toISOString()) 
            utils.setMessage('O tempo de produção não pode ser 0, verifique o inicio e fim do movimento!', 'error', this.lbMessage)
        else isValid = true
        if (!isValid) utils.invalidateInputs([this.fields.inimov, this.fields.fimmov])
        return isValid
    }

    // validação de embalagens (sorbrescrever)
    validatePackages = () => true

    // Calcula total do apontamento (sobrescrever)
    getFullQtdReport = () => 0

    // Pega o id de um valor
    getIdValue = value => parseInt(value.split('-')[0])

    
}


// Construtor Modal de seleção de O.P
function OpModal(form){
    this.form = form
    this.opModal = document.querySelector('#opModal')
    this.loading = this.opModal.querySelector('.loading')
    this.modalBody = this.opModal.querySelector('#opTableBody')
    this.btClose = this.opModal.querySelector('#closeModalOp')
    this.listOPs
    this.isOpened = false
    this.URL = opModal.dataset.url
    this.request = {codpro:'', codori:'', numorp:''}

    // Abre modal
    this.open = async () => { 
        if (!this.isOpened) this.opModal.classList.remove('hidden') 
        this.modalBody.innerHTML = ''
        this.loading.classList.remove('hidden')
        await this.requestOPs()
        this.renderOPs()
        this.loading.classList.add('hidden')  
    }

    // fecha modal
    this.close = () => this.opModal.classList.add('hidden')
    this.btClose.addEventListener('click', this.close)

    // solicita lista de O.Ps do banco de dados
    this.requestOPs = async () => {
        this.setFiltersOP()
        try {
            this.listOPs = await utils.ajaxRequest(this.URL, this.request)
        } catch (e) {
            console.error('Erro na requisição ao servidor'+e.message)
            this.listOPs = []
        }
    }

    
    // Renderiza O.Ps no HTML
    this.renderOPs = () => {
        if (this.listOPs.length === 0){ 
            this.modalBody.innerHTML = `<tr><td colspan="5" class="text-center py-8 px-4 text-gray-600">Não foram encontrados ordens de produção nesses filtros</td></tr>`;
            return
        }

        let LSitOrp = {L:"Liberada", A:"Em Andamento"}
        this.listOPs.forEach(OP => {
            if (!this.form.fields.codori.isScope(OP.codori)) return
            let row = document.createElement('tr')
            row.className = "cursor-pointer hover:bg-gray-200"
            row.innerHTML = `
                <td class="px-4 py-2 border">${OP.numorp}</td>
                <td class="px-4 py-2 hidden md:block border">${LSitOrp[OP.sitorp]}</td>
                <td class="px-4 py-2 border">${OP.codori}</td>
                <td class="px-4 py-2 hidden md:block border">${OP.codpro}</td>
                <td class="px-4 py-2 border">${new Date(OP.datger).toLocaleDateString("pt-BR")}</td>
            `;
            row.onclick = () => this.selectOP(OP)
            this.modalBody.appendChild(row) 
        })
    }

    // Define filtros com base em campos já preenchidos
    this.setFiltersOP = () => {
        this.request.codpro = this.form.fields.codpro.value || ''
        this.request.codori = this.form.fields.codori.value || ''
    }

    // função de seleção de uma O.P
    this.selectOP = (OP) => {
        this.form.fields.codpro.value = OP.codpro
        this.form.fields.codori.value = OP.codori
        this.form.fields.numorp.value = OP.numorp 
        this.form.validateOP()
        this.close()
    } 
}


