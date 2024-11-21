import * as utils from './utils.js'; 

// Construtor modal de confirmação
export function ConfirmationModal(title, message, onConfirm){
    this.modal = document.createElement("div");
    this.modal.innerHTML = `
        <div class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
            <div class="bg-white rounded-lg shadow-lg w-[450px]">
                <div class="flex flex-col">
                    <div class="bg-emerald-600 rounded-t-lg py-2 px-6 text-center">
                        <h2 class="text-2xl font-semibold text-white">${title}</h2>
                    </div>
                    <div class="bg-gray-50 p-5 rounded-b-lg">
                        <p class="text-center text-gray-700 font-semibold my-4">${message}</p>
                        <div class="flex justify-center space-x-20">
                            <button id="cancelAction" class="text-lg px-3 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 transition duration-300 shadow-md">
                                Cancelar
                            </button>
                            <button id="confirmAction" class="text-lg px-3 py-2 bg-emerald-600 text-white rounded-md hover:bg-green-700 transition duration-300 shadow-md">
                                Confirmar
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    this.btCancel = this.modal.querySelector('#cancelAction')
    this.btConfirm = this.modal.querySelector('#confirmAction')
    this.btCancel.addEventListener("click", () => this.modal.remove())
    this.btConfirm.addEventListener("click", () => { onConfirm(); this.modal.remove() })

    document.body.appendChild(this.modal)
}


// Construtor Modal de leitura de QR CODE
export function QRCodeModal(checkExists, onConfirm){

    this.onConfirm = onConfirm
    this.timeOut = 15
    this.timeCounter = 0
    this.counter
    this.checkExists = checkExists

    // Inicializa componentes
    this.initializeElements = () => {
        this.modal = document.createElement('div')
        this.modal.className = "fixed inset-0 bg-gray-800 bg-opacity-75 flex items-center justify-center"
        this.modal.innerHTML = `<div class="bg-white rounded-lg shadow-lg overflow-hidden w-auto">
                <div class="bg-emerald-600 text-white flex items-center justify-between px-3 py-2">
                    <h2 id="modal-title" class="text-lg font-semibold">Leitura de Embalagem</h2>
                </div>
                <div class="p-6 space-y-4">
                    <div id="qrcode-container" class="flex justify-center">
                        <div class="flex flex-col items-center bg-gray-100 p-6 rounded-2xl shadow-xl max-w-sm mx-auto">
                            <div class="relative">
                                <div class="absolute inset-0 border-[6px] border-dashed border-emerald-600 rounded-lg animate-pulse"></div>
                                <video width="300" class="rounded-lg shadow-md border border-gray-300"></video>
                            </div>
                            <div class="flex justify-center items-center py-4 loading hidden" role="status"></div>   
                            <p id="message" class="text-sm mt-4"></p>
                        </div>
                    </div>
                    <canvas hidden></canvas>
                    <div id="codigo-manual-container" class="mt-4">
                        <input type="text" id="codigo-manual" class="border border-gray-300 px-4 py-2 rounded w-full text-center focus:outline-none focus:ring-2 focus:ring-emerald-500" placeholder="Ou digite o código abaixo">
                    </div>
                </div>
                <div class="flex justify-between bg-gray-100 p-4">
                    <button id="btClose" class="px-4 py-2 bg-red-600 text-white font-semibold rounded-md hover:bg-red-500">Fechar</button>
                    <button id ="btConfirm" class="ml-2 px-4 py-2 bg-emerald-600 text-white font-semibold rounded-md hover:bg-emerald-500">Confirmar</button>
                </div>
            </div>`

            this.video = this.modal.querySelector('video')
            this.canvas = this.modal.querySelector('canvas')
            this.canvasContext = this.canvas.getContext('2d');
            this.inputCode = this.modal.querySelector('#codigo-manual')
            this.lbMessage = this.modal.querySelector('#message')
            this.btClose = this.modal.querySelector('#btClose')
            this.btClose.addEventListener('click', this.close)
            this.btConfirm = this.modal.querySelector('#btConfirm')
            this.btConfirm.addEventListener('click', this.confirm)
            this.loading = this.modal.querySelector('.loading')
            document.body.appendChild(this.modal)
    }

    // Inicializa video
    this.startVideo = () => {
        // Validação dos objetos de midia do dispositivo
        if (!(navigator.mediaDevices && navigator.getUserMedia)){
            console.error("Objetos de midia do dispositivo não forão encontrados! verifique se a conexão é HTTPS.");
            utils.setMessage("Não foi possível obter acesso a câmera! verifique se a sua conexão é segura.", 'error', this.lbMessage)
            return
        }
        // Inicialização do video
        utils.isLoading(this.loading, true)
        navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } })
        .then(stream => {
            utils.clearMessage(this.lbMessage)
            this.video.srcObject = stream
            this.video.setAttribute("playsinline", true);
            this.video.play(); 
            this.setCounter();
            requestAnimationFrame(this.detectQRCode)
        })
        .catch(error => {
            console.error("Erro ao acessar a câmera:", error)
            utils.setMessage("Erro ao acessar a câmera!", 'error', this.lbMessage)
        }) 
        utils.isLoading(this.loading, false)
    }

    // Detecta QR Code
    this.detectQRCode = () => {
        if (this.video.readyState === this.video.HAVE_ENOUGH_DATA) {
            this.canvasContext.drawImage(this.video, 0, 0, this.canvas.width, this.canvas.height)
            const imageData = this.canvasContext.getImageData(0, 0, this.canvas.width, this.canvas.height);
            const code = jsQR(imageData.data, imageData.width, imageData.height);
            if (code && this.inputCode.value !== code.data) this.detected(code)
        }
        requestAnimationFrame(this.detectQRCode)
    }

    // QR Code detectado
    this.detected = code => {
        if (this.checkExists(code.data)) return
        this.video.pause()
        utils.setMessage('<strong class="text-lg">NOVO QR CODE DETECTADO</strong>', 'success', this.lbMessage)
        utils.validateInputs([this.inputCode])
        this.inputCode.value = code.data
        setTimeout(() => this.video.play(), 300)
        setTimeout(() => utils.clearMessage(this.lbMessage), 3000)
    }

    // define contador para tempo de leitura
    this.setCounter = () => { 
            this.timeCounter = 0; 
            clearInterval(this.counter)
            this.counter = setInterval(() => { 
                if (this.timeCounter >= this.timeOut) {
                    clearInterval(this.counter)
                    if(!this.inputCode.value && !this.lbMessage.textContent) utils.setMessage("Nenhum QR Code foi detectado!", 'error', this.lbMessage);
                } else this.timeCounter++
            }, 1000)
    }

    // leitura manual
    this.confirm = async () => {
        utils.clearMessage(this.lbMessage)
        utils.isLoading(this.loading, true)
        utils.validateInputs([this.inputCode])
        if (!this.inputCode.value) utils.invalidateInputs([this.inputCode])
        let response = await this.onConfirm(this.inputCode.value)
        if(response) {
            utils.invalidateInputs([this.inputCode])
            utils.setMessage(response, 'error', this.lbMessage)
        } else this.inputCode.value = ''
        this.setCounter()
        utils.isLoading(this.loading, false)
    }

    // Fecha o modal 
    this.close = () => {
        this.timeCounter = this.timeOut
        this.video.srcObject?.getTracks().forEach(track => track.stop())
        this.video.pause()
        this.video.srcObject = null
        this.modal.remove()
    }

    // Abre o modal
    this.open = () => {
        this.initializeElements()
        this.startVideo()
    }
}

