import { ajaxRequest } from '../../geral/js/utils.js';

// Construtor do auto Complete de campos do formulário
export function AutoComplete(input, production_Script) {
    this.input = input;
    this.URL = input.dataset.url
    this.field = input.id
    this.option = null
    this.parent_div = input.parentNode
    this.listSuggestion = new ListSuggestion(this.field, this.parent_div)
    this.filtersDB = {}
    this.escludesDB = {}
    this.filters = {}
    this.filteredListOption = []
    this.useScript = true ? input.className.includes("roteiro") : false
    this.focus = true ? input.className.includes("focus") : false
    this.production_Script = production_Script
    this.listOptions = [];    

    // Iinicia o auto complete
    this.start = () => {
        this.input.addEventListener('input', async e => {
            await this.updateSuggestions(e);
            this.renderSuggestions();
        });
        if (this.focus){
                this.input.addEventListener('focus', async e => {
                await this.updateSuggestions(e);
                this.renderSuggestions();
            });
        }

        this.input.addEventListener('blur', e => setTimeout(this.finallyAutoComplete, 200))
    }

    // atualiza sugestões do auto complete
    this.updateSuggestions = async e => {
        let textFilter = this.input.value.toUpperCase();
        if (!textFilter && !this.focus) return;
        if (this.useScript && !this.production_Script) return;

        if (this.useScript) this.listOptions = this.production_Script
        else if ((textFilter.length === 1 || this.listOptions.length === 0) && e.inputType !== 'deleteContentBackward')
            try {
                this.listOptions = await ajaxRequest(this.URL, {texto: textFilter, filtros:this.filtersDB, exclusoes:this.escludesDB})
            } catch { this.listOptions = [] }
         
        this.filteredListOption = this.filterListOption(textFilter)
    }

    // renderiza sugestões do auto complete
    this.renderSuggestions = () => {
        if (!this.listSuggestion.isOpened) this.listSuggestion.open()
        this.listSuggestion.clear()
        let addeds = []

        this.filteredListOption.forEach(option => {
            let textSuggestion = option[this.field]
            if (addeds.includes(textSuggestion)) return;
            let suggestion = document.createElement('li')
            suggestion.className = 'p-2 hover:bg-gray-100 cursor-pointer'
            suggestion.textContent = textSuggestion
            suggestion.onclick = () => [this.option, this.input.value] = [option, textSuggestion]
            this.listSuggestion.addSuggestion(suggestion)
            addeds.push(textSuggestion)
        })
    }
    
    // finaliza o auto complete
    this.finallyAutoComplete = () => {
        let option = this.filteredListOption.filter(option => option[this.field] === this.input.value)
        if (option.length > 0) this.option = option[0]
        else if (this.filteredListOption.length === 1 && !this.option && this.input.value !== "") {
            this.option = this.filteredListOption[0]
            this.input.value = this.option[this.field]
        }
        else this.option = null
        
        this.listSuggestion.close()
    }

    // filtra registros da lista de sugestões
    this.filterListOption = (text) => {
        let filteredListOption = this.listOptions.filter(option => {
            if (!option[this.field].toUpperCase().includes(text)) return false
            return true
        })
        if (Object.values(this.filters).length === 0) return filteredListOption
        filteredListOption = filteredListOption.filter(option => {
            for (let filterKey in this.filters) {
                let filter = this.filters[filterKey]
                if (Array.isArray(filter)) { if(!filter.includes(option[filterKey])) return false }
                else if (!(option[filterKey] === filter)) { return false }
            }
            return true
        })
        return filteredListOption
    }

    this.setFilters = (filters) => this.filters = {...this.filters, ...filters}
    this.setFiltersDB = (filters) => this.filtersDB = {...this.filtersDB, ...filters}
    this.setExcludesDB = (excludes) => this.escludesDB = {...this.escludesDB, ...excludes}

    this.start();
}

// Construtor da lista de sugestões do auto complete
function ListSuggestion(field, parent_div){
    this.idList = field+"-list"
    this.ElListSuggestions = document.createElement('ul')
    this.ElListSuggestions.className = "hidden absolute z-10 bg-white border border-gray-300 w-full rounded-md mt-1 overflow-y-auto max-h-[200px]"
    this.ElListSuggestions.id = this.idList
    this.isOpened = false
    parent_div.appendChild(this.ElListSuggestions)

    // abre lista de sugestões
    this.open = () => { this.ElListSuggestions.classList.remove("hidden"); this.isOpened = true }
    // fecha lista de sugestões
    this.close = () => { this.ElListSuggestions.classList.add("hidden"); this.isOpened = false }
    // limpa lista de sugestões
    this.clear = () => this.ElListSuggestions.innerHTML = ''
    // adiciona sugestão a lista
    this.addSuggestion = suggestion => this.ElListSuggestions.appendChild(suggestion)
}



