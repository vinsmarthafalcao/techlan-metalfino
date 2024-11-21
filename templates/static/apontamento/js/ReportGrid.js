import { ajaxRequest } from "../../geral/js/utils.js"

export function ReportGrid(){
    this.reportGrid = document.getElementById('embalagens-container')
    this.URL = this.reportGrid.dataset.url
    this.OP = null
    this.lote = null
    this.cardsReport = []

    // adiciona card de apontamento de embalagem
    this.addCardReport = packageRead => {
        let newPackage = new ReportPackage(packageRead, this.OP.codpro, {coddep:this.OP.coddep, desdep:this.OP.desdep})
        newPackage.btRemove.onclick = () => this.removeCardReport(newPackage)
        this.cardsReport.push(newPackage)
        this.reportGrid.appendChild(newPackage.NodeCard)
    }

    // define a OP que os cards devem respeitar
    this.setOP = OP => {
        this.OP = OP
        this.OP.componentes.forEach(component => component.proportion = component.qtdprv/OP.qtdprv)
    }

    // retorna embalagem do banco de dados
    this.getPackage = async codePackage => {
        // Valida formato do codigo da embalagem
        if (!this.validateCodePackage(codePackage))
            return "Código de embalagem não é válido!"
        // valida se a embalagem já foi lida
        if (this.packagesExists(codePackage)) return "Embalagem já foi lida!"
        // busca embalagem no banco de dados
        let response = await ajaxRequest(this.URL, codePackage)
        if (! response) return "Código inserido não corresponde uma embalagem no sistema!"   
        else if (response.sitemb === 'T') return "Embalagem ainda não foi recebida!"
        else if (response.sitemb === 'F') return "Embalagem está finalizada!"
        // Valida se é componente da OP
        let component = this.isComponentOP(response.codpro)
        if(!component) return "O produto da embalagem lida não é componente da O.P selecionada!" 
        // Valida lote
        if (!this.lote) this.lote = response.codlot
        else if (response.codlot !== this.lote) 
            return "Embalagens lidas em um mesmo apontamento devem ter o mesmo lote!"
        // Cria card de embalagem
        response.proportion = component.proportion
        this.addCardReport(response)

    }

    // valida formato do código da embalagem
    this.validateCodePackage = codePackage => { 
        let validation = codePackage.match(/^(\d{4})(\d{2})(\d{2})(\d+)\.(\d+)$/)
        return false ? !validation : true
    }

    // remove card de apontamento de embalagem
    this.removeCardReport = cardReport => {
        this.cardsReport.splice(this.cardsReport.indexOf(cardReport), 1)
        this.reportGrid.removeChild(cardReport.NodeCard)
        if (this.cardsReport.length === 0) this.lote = null
    }  

    // Valida se a embalagem ja foi lida
    this.packagesExists = codePackage => {
        let testExists = this.cardsReport.filter(cardReport => 
            cardReport.packageRead.numemb === parseInt(codePackage.split('.')[0]) && cardReport.packageRead.veremb === parseInt(codePackage.split('.')[1]))
            return true ? testExists.length > 0 : false
    }

    // Valida se é componente da O.P selecionada
    this.isComponentOP = codpro => {
        for (let component of this.OP.componentes) if(component.codcmp === codpro) return component
        return null
    }

     // Totaliza quantidades dos apontamentos
     this.sumarizeReports = () => 
        this.cardsReport.reduce((acc, card) => acc + (parseInt(card.ipQtd1Qld.value) || 0) + (parseInt(card.ipQtdRfg.value) || 0), 0)
     

    // remove todas os cards
    this.clear = () => {
        this.cardsReport.forEach(cardReport => this.reportGrid.removeChild(cardReport.NodeCard))
        this.cardsReport.length = 0
    }
    
    // imprime etiquetas das embalagens que ainda tem quantidades
    this.printTags = async estagio => {
        let packageKeys = []
        this.cardsReport.forEach(card => {
            if (!card.created) return
            packageKeys.push({numemb: card.packageRead.numemb, veremb:card.packageRead.veremb})
            if (card.packageReport) 
                packageKeys.push({numemb: card.packageReport.numemb, veremb:card.packageReport.veremb})
        })

        let request = {
            estagio: estagio,
            chavesEmbalagem: packageKeys
        }

        let response = await ajaxRequest('/apontamento/imprimirEmbalagens', request)
        if (!response.error) {
            this.cardsReport.forEach(card => card.printed = true)
        }
        return response
    } 
   
}

// Construtor Card de apontamento de embalagem
function ReportPackage(packageRead, codpro, deposito){
    this.packageRead = packageRead
    this.packageReport = null
    this.codpro = codpro
    this.deposito = deposito 
    this.created = false
    this.printed = false

    // Definição de componentes do card de embalagem  
    this.NodeCard = document.createElement('div')
    this.NodeCard.className = "bg-white shadow-md border border-gray-300 rounded-lg w-full"
    this.NodeCard.innerHTML = document.getElementById('template-embalagem-apt').innerHTML
    this.btRemove = this.NodeCard.querySelector('button')
    this.ipQtd1Qld = this.NodeCard.querySelector('.qtd1qld') 
    this.ipQtdRfg = this.NodeCard.querySelector('.qtdrfg')
    this.lbNumEmbL = this.NodeCard.querySelector('.numembLido')
    this.lbNumEmbP = this.NodeCard.querySelector('.numembPro')
    this.ipCodProL = this.NodeCard.querySelector('.codproLido')
    this.ipQtdEmbL = this.NodeCard.querySelector('.qtdembLido')
    this.ipCodProP = this.NodeCard.querySelector('.codproPro')
    this.ipBalance = this.NodeCard.querySelector('.saldo')
    this.ipQtd1Qld.value = (this.packageRead.qtdemb/this.packageRead.proportion) | 0;
    this.ipQtdRfg.value = 0
    
    // Atualiza HTML do card
    this.update = () => {
        this.lbNumEmbL.textContent = `${this.packageRead.numemb}.${this.packageRead.veremb}`
        this.lbNumEmbP.textContent = `${this.packageRead.numemb}.${this.packageRead.veremb}`
        this.ipCodProL.value = this.packageRead.codpro
        this.ipQtdEmbL.value = this.packageRead.qtdemb
        this.ipCodProP.value = this.codpro
        this.updateBalance()
    }

    // Atualiza saldo do card
    this.updateBalance = () => {
        let qtdembl = parseInt(this.ipQtdEmbL.value) || 0
        let qtd1qld = parseInt(this.ipQtd1Qld.value) || 0
        let qtdrfg = parseInt(this.ipQtdRfg.value) || 0
        this.ipBalance.value = qtdembl - (qtd1qld + qtdrfg) * this.packageRead.proportion
        // this.validateBalance()
        this.updateCodePackage()
    }

    // Validação das quantidades
    this.validateBalance = () => {
        if (parseInt(this.ipBalance.value) < 0){
            this.ipQtd1Qld.value = this.packageRead.qtdemb/this.packageRead.proportion
            this.ipQtdRfg.value = 0
            this.ipBalance.value = 0
        }
    }

    // Atualiza codigo da embalagem gerada
    this.updateCodePackage = () => {
        if (this.ipBalance.value > 0){
            this.lbNumEmbP.textContent = `${this.packageRead.numemb}.X`
            this.lbNumEmbP.classList.add('text-blue-500')
        } else {
            this.lbNumEmbP.textContent = `${this.packageRead.numemb}.${this.packageRead.veremb}`
            this.lbNumEmbP.classList.remove('text-blue-500')
        }
    }

     // Confirmação das informações após apontamento da embalagem
     this.confirmPackage = packageConfirmed => {
        if (packageConfirmed.veremb !== this.packageRead.veremb) {
            this.packageReport = packageConfirmed
            this.lbNumEmbP.textContent = `${this.packageReport.numemb}.${this.packageReport.veremb}`
        }
        this.codpro = packageConfirmed.codpro
        this.deposito.coddep = packageConfirmed.coddep
        this.created = true
    }

    // Define eventos de atualização de saldo
    this.NodeCard.querySelector('.qtd1qld').addEventListener('blur', this.updateBalance)
    this.NodeCard.querySelector('.qtdrfg').addEventListener('blur', this.updateBalance)

    this.update()
}
