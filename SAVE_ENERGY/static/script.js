// ==========================
// VARIABLES GLOBALES
// ==========================
let realtimeLabels = []
let realtimeData = []
let realtimeChart = null

// ==========================
// INIT
// ==========================
window.onload = ()=>{
    if(document.getElementById("realtimeChart")){
        initRealtimeChart()
        setInterval(checkAnomaly,3000)
    }

    // Cargar lista si está en página delete
    if(document.getElementById("machineSelect")){
        loadMachinesForDelete();
    }
}

// ==========================
// GUARDAR MÁQUINA
// ==========================
function saveMachine(){

    const data = {
        codigo: document.getElementById('codigo').value,
        modelo: document.getElementById('modelo').value,
        tipo: document.getElementById('tipo').value,
        pkw: document.getElementById('pkw').value,
        php: document.getElementById('php').value,
        voltaje: document.getElementById('voltaje').value,
        fases: document.getElementById('fases').value,
        frecuencia: document.getElementById('frecuencia').value,
        corriente: document.getElementById('corriente').value,
        fp: document.getElementById('fp').value,
        eficiencia: document.getElementById('eficiencia').value,
        anio: document.getElementById('anio').value,
        horas: document.getElementById('horas').value,
        ubicacion: document.getElementById('ubicacion').value,
        estado: document.getElementById('estado').value,
        instalacion: document.getElementById('instalacion').value,
        mantenimiento: document.getElementById('mantenimiento').value,
        obs: document.getElementById('obs').value
    };

    fetch('/save_machine', {
        method: 'POST',
        headers:{ 'Content-Type':'application/json' },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        if(result.status === "ok"){
            alert("✅ La información de la máquina fue guardada correctamente");
        }else{
            alert("❌ Error al guardar la información");
        }
    })
    .catch(error => {
        console.error(error);
        alert("❌ Error de conexión con el servidor");
    });
}

// ==========================
// VERIFICAR MÁQUINA (VISUAL)
// ==========================
function searchMachine(){

    const code = document.getElementById('search_code').value;
    const model = document.getElementById('search_model').value;

    let url = "";

    if(code){
        url = `/machine/code/${code}`;
    }else if(model){
        url = `/machine/model/${model}`;
    }else{
        alert("Ingrese código o nombre de máquina");
        return;
    }

    fetch(url)
    .then(res => res.json())
    .then(data => {

        const resultDiv = document.getElementById('result');
        resultDiv.innerHTML = "";

        // --- BÚSQUEDA ÚNICA ---
        if(!Array.isArray(data)){

            if(data.error){
                resultDiv.innerHTML = "<p style='color:red;'>❌ Máquina no encontrada</p>";
                return;
            }

            resultDiv.innerHTML = renderMachineCard(data);
        }
        // --- BÚSQUEDA MÚLTIPLE ---
        else{
            if(data.length === 0){
                resultDiv.innerHTML = "<p style='color:red;'>❌ No se encontraron máquinas</p>";
                return;
            }

            let html = "";
            data.forEach(m => {
                html += renderMachineCard(m);
            });

            resultDiv.innerHTML = html;
        }
    })
    .catch(err=>{
        console.error(err);
        document.getElementById('result').innerHTML = "<p style='color:red;'>❌ Error en la búsqueda</p>";
    });
}

// ==========================
// TARJETA VISUAL
// ==========================
function renderMachineCard(m){
    return `
    <div style="
        border:1px solid #FFD700;
        border-radius:10px;
        padding:15px;
        margin-bottom:20px;
        background:rgba(0,0,0,0.3);
        color:white;
    ">
        <h3>🏭 Máquina Registrada</h3>
        <p><b>Código:</b> ${m.internal_code}</p>
        <p><b>Modelo:</b> ${m.model}</p>
        <p><b>Tipo:</b> ${m.type}</p>

        <hr>

        <p><b>Potencia:</b> ${m.power_kw} kW / ${m.power_hp} HP</p>
        <p><b>Voltaje:</b> ${m.voltage} V</p>
        <p><b>Fases:</b> ${m.phases}</p>
        <p><b>Frecuencia:</b> ${m.frequency}</p>
        <p><b>Corriente:</b> ${m.current}</p>

        <hr>

        <p><b>Ubicación:</b> ${m.location}</p>
        <p><b>Estado:</b> ${m.status}</p>

        <hr>

        <p><b>Instalación:</b> ${m.install_date}</p>
        <p><b>Mantenimiento:</b> ${m.last_maintenance}</p>

        <hr>

        <p><b>Observaciones:</b> ${m.observations}</p>
    </div>
    `;
}

/* =====================================================
   ================ ELIMINACIÓN SEGURA ==================
   ===================================================== */

// ==========================
// CARGAR MÁQUINAS PARA BORRAR
// ==========================
async function loadMachinesForDelete(){
    const res = await fetch('/machines_list');
    const data = await res.json();

    const select = document.getElementById("machineSelect");
    if(!select) return;

    select.innerHTML = '<option value="">-- Seleccione una máquina --</option>';

    data.forEach(m=>{
        const opt = document.createElement("option");
        opt.value = m.id;
        opt.innerText = `${m.code} | ${m.model} | ID:${m.id}`;
        select.appendChild(opt);
    });
}

// ==========================
// CONFIRMAR BORRADO
// ==========================
async function confirmDelete(){

    const id = document.getElementById("machineSelect").value;
    const key = document.getElementById("deleteKey").value;
    const msg = document.getElementById("deleteMsg");

    if(!id){
        msg.innerText = "❌ Seleccione una máquina";
        msg.style.color = "red";
        return;
    }

    if(!key){
        msg.innerText = "❌ Ingrese la clave de seguridad";
        msg.style.color = "red";
        return;
    }

    if(!confirm("⚠️ ¿Está seguro de eliminar esta máquina?\n\nEsta acción es irreversible.")){
        return;
    }

    const res = await fetch('/delete_machine',{
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body: JSON.stringify({id:id, key:key})
    });

    const data = await res.json();

    if(data.status === "ok"){
        msg.innerText = "✅ Máquina eliminada correctamente";
        msg.style.color = "lime";
        document.getElementById("deleteKey").value = "";
        loadMachinesForDelete();
    }else{
        msg.innerText = "❌ " + data.message;
        msg.style.color = "red";
    }
}


// ==========================
// REALTIME DATA
// ==========================
let timeLabels = [];
let voltageData = [];
let currentData = [];
let realtimeChartRT = null;

// ==========================
// INIT REALTIME GRAPH
// ==========================
function initRealtimeGraph(){

    const ctx = document.getElementById('realtimeChart');
    if(!ctx) return;

    realtimeChartRT = new Chart(ctx, {
        type: 'line',
        data: {
            labels: timeLabels,
            datasets: [
                {
                    label: 'Voltaje (V)',
                    data: voltageData,
                    borderWidth: 2,
                    tension: 0.3
                },
                {
                    label: 'Corriente (A)',
                    data: currentData,
                    borderWidth: 2,
                    tension: 0.3
                }
            ]
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    title: { display:true, text:'Tiempo' }
                },
                y: {
                    title: { display:true, text:'Valor' }
                }
            }
        }
    });

    loadRealtimeHistory();
}

// ==========================
// GUARDAR REALTIME
// ==========================
function saveRealtime(){

    const voltage = document.getElementById('voltageInput').value;
    const current = document.getElementById('currentInput').value;

    if(!voltage || !current){
        alert("Ingrese voltaje y corriente");
        return;
    }

    fetch('/save_realtime',{
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body: JSON.stringify({
            voltage: voltage,
            current: current
        })
    })
    .then(res=>res.json())
    .then(data=>{
        if(data.status === "ok"){
            loadRealtimeHistory();
        }else{
            alert("Error guardando datos");
        }
    });
}

// ==========================
// CARGAR HISTORICO
// ==========================
function loadRealtimeHistory(){

    fetch('/realtime_data')
    .then(res=>res.json())
    .then(data=>{

        timeLabels.length = 0;
        voltageData.length = 0;
        currentData.length = 0;

        data.forEach(d=>{
            timeLabels.push(d.timestamp);
            voltageData.push(d.voltage);
            currentData.push(d.current);
        });

        if(realtimeChartRT){
            realtimeChartRT.update();
        }
    });
}

// ==========================
// AUTO INIT
// ==========================
window.addEventListener('load', ()=>{
    initRealtimeGraph();
});
