import { ajaxRequest } from "./utils.js"

export function PackageGrid(){
    this.packageGrid = document.getElementById('embalagens-container')
    this.URL = this.packageGrid.dataset.url
    this.deposito = {coddep:null, desdep:null}
    this.produto = null
    this.dataNum = null
    this.packages = []

    // adiciona embalagem
    this.addPackage = () => {
        let newPackage = new Package(this.dataNum.slice(0, 10).replace(/-/g, '')+'XXXX', 1, this.produto, null, null, this.deposito)
        newPackage.btRemove.onclick = () => this.removePackage(newPackage)
        this.packages.push(newPackage)
        this.packageGrid.appendChild(newPackage.NodePackage)
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
        else if (response.sitemb === 'R') return "Embalagem já possui o status de Recebida!"
        else if (response.sitemb === 'F') return "Embalagem está finalizada!"
        // Define o depósito padrão dessa grid
        if (this.packages.length === 0)
            this.deposito.coddep = response.coddep, this.deposito.desdep = response.desdep
        else if (response.coddep !== this.deposito.coddep) return "Todas as embalagens lidas devem está no mesmo depósito!"
        // cria embalagem na grid
        let newPackage = new Package(
            response.numemb, 
            response.veremb, 
            response.codpro, 
            response.codlot,
            response.sitemb,
            {coddep: response.coddep, desdep: response.desdep},
            parseInt(response.qtdemb),
            response.histemb
        )
        newPackage.inpQtdEmb.setAttribute('disabled', true)
        newPackage.btRemove.onclick = () => this.removePackage(newPackage)
        newPackage.created = true
        this.packages.push(newPackage)
        this.packageGrid.appendChild(newPackage.NodePackage)
    }

    // valida formato do código da embalagem
    this.validateCodePackage = codePackage => { 
        let validation = codePackage.match(/^(\d{2})(\d{2})(\d{2})(\d{4})\.(\d+)$/)
        return false ? !validation : true
    }

    // Valida se a embalagem ja foi lida
    this.packagesExists = codePackage => {
        let testExists = this.packages.filter(packageItem => 
            packageItem.numemb === parseInt(codePackage.split('.')[0]) && packageItem.veremb === parseInt(codePackage.split('.')[1]))
        return true ? testExists.length > 0 : false
    }
    

    // remove embalagem
    this.removePackage = packageRemoved => {
        this.packages.splice(this.packages.indexOf(packageRemoved), 1)
        this.packageGrid.removeChild(packageRemoved.NodePackage)
    }  

    // remove todas as embalagens
    this.clear = () => {
        this.packages.forEach(packageRemoved => this.packageGrid.removeChild(packageRemoved.NodePackage))
        this.packages.length = 0
    }
    
    // sumariza embalagens
    this.sumarizePackages = () => 
        this.packages.reduce((acc, packageItem) => acc + (parseInt(packageItem.inpQtdEmb.value) || 0), 0)

    // imprime etiquetas das embalagens
    this.printTags = async estagio => {
        let packageKeys = this.packages.map(packageItem => 
            packageItem.created && packageItem.qtdemb > 0 && {numemb: packageItem.numemb, veremb:packageItem.veremb})
        
        let request = {
            estagio: estagio,
            chavesEmbalagem: packageKeys
        }
        let response = await ajaxRequest(this.URL, request)
        if (!response.error) {
            for (let i in response.chavesEmbalagem)
                this.packages[i].printed = response.chavesEmbalagem[i].printed
        }
        return response
    
    } 
   
}

// Construtor das embalagens
function Package(numemb, veremb, codpro, codlot=null, sitemb=null, deposito, qtdemb=null, histemb){
    this.codpro = codpro
    this.deposito = deposito
    this.sitemb = sitemb || ''
    this.codlot = codlot || ''
    this.numemb = null
    this.veremb = null
    this.qtdemb = qtdemb
    this.history = histemb
    this.created = false 
    this.printed = false

    // Definição de componentes do card de embalagem  
    this.setComponents = () => {
        this.NodePackage = document.createElement('div')
        this.NodePackage.innerHTML = document.getElementById('template-embalagem').innerHTML
        this.lbNumEmb = this.NodePackage.querySelector('h5')
        this.inpQtdEmb = this.NodePackage.querySelector('.embqtdemb')
        this.btRemove = this.NodePackage.querySelector('button')
        this.updatePackage()
    }

    // Atualizar informações da embalagem
    this.updatePackage = () => {
        this.NodePackage.querySelector('.embcodpro').textContent = this.codpro || ''
        if (this.NodePackage.querySelector('.embnumorp'))
            this.NodePackage.querySelector('.embnumorp').textContent = `${this.history?.codori}-${this.history?.numorp}` || ''
        this.NodePackage.querySelector('.embcoddep').textContent = this.deposito?.desdep || ''
        if (this.NodePackage.querySelector('.embcodlot'))
            this.NodePackage.querySelector('.embcodlot').textContent = this.codlot
        if (this.NodePackage.querySelector('.embsitemb'))
            this.NodePackage.querySelector('.embsitemb').textContent = this.sitemb
        this.inpQtdEmb.value = this.qtdemb || ''

    }

    // Confirmação das informações após apontamento da embalagem
    this.confirmPackage = packageConfirmed => {
        this.setNumEmb(packageConfirmed.numemb, packageConfirmed.veremb)
        this.codlot = packageConfirmed.codlot
        this.codpro = packageConfirmed.codpro
        this.deposito.coddep = packageConfirmed.coddep
        this.qtdemb = parseInt(packageConfirmed.qtdemb)
        this.updatePackage()
        this.created = true
    }

    // Definição da situação da embalagem
    // this.setSituation = situacao => {
    //     this.situacao = situacao
    //     const LSitEmb = {T:"A Transferir", R:"Recebida", F:"Finalizada"}
    //     const InpSitEmb = this.NodePackage.querySelector('.embsitemb')
    //     InpSitEmb.parentElement.classList.remove("hidden")
    //     InpSitEmb.textContent = LSitEmb[this.situacao]
    // }

    // Define lote
    // this.setLot = lote => {
    //     this.codlot = lote
    //     const inpLote = this.NodePackage.querySelector('.embcodlot')
    //     inpLote.parentElement.classList.remove("hidden")
    //     inpLote.textContent = this.codlot
    // }

    // Seta numero de embalagem
    this.setNumEmb = (numemb, veremb) => { 
        this.numemb = numemb 
        this.veremb = veremb
        this.lbNumEmb.textContent = `Emb. ${numemb}.${veremb}`; 
    }    

    this.setComponents()
    this.setNumEmb(numemb, veremb)        
}

