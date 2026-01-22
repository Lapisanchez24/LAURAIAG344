function downloadPDF() {

    const element = document.querySelector('#pdf-content');
     
    const otp = {
        margin:       [10, 5, 15, 5],// [arriba, izquierda, abajo, derecha] en mm
        filename:     'Hoja_de_Vida_Laura_Sanchez_Galvis.pdf',
        image:        { type: 'jpeg', quality: 1 }, // Calidad máxima
        html2canvas:  { scale: 2,
                        useCORS: true,
                        scrollY: 0    
        }, // Mejora la resolución

        jsPDF:{ 
            unit: 'mm', 
            format: 'a4', 
            orientation: 'portrait'  //Orientación vertical
        }
    }
    html2pdf().set(otp).from(element).save();
}