
function buscarPiso() {
    let id = document.getElementById('hotel').value
    fetch(`/find-hotel/${id}`)
    .then(res => res.json())
    .then(data => {
        generarOptions(data.pisos)
    })
    
}

function buscarHabitacion(){
    let id = document.getElementById('room_id').value
    
    fetch(`/find-room/${id}`)
        .then(res => res.json())
        .then(data => {
            let template = ''
            template += `
                <form action="/update-room" method="POST">                   
                    <input type="hidden" name="id" value="${data.id}" />
                    <label for="" class="form-label mt-2">Floor</label>
                    <input name="piso" id="pisos" class="form-control" value="${data.piso}" />
    
                    <label for="" class="form-label mt-2">Number room</label>
                    <input type="number" name="numero" id="" class="form-control" value="${data.numero}">
    
                    <label for="" class="form-label mt-2">Capacity</label>
                    <input type="number" name="capacidad" id="" class="form-control" value="${data.capacidad}">

                    <label for="" class="form-label mt-2">Price</label>
                    <input type="number" name="precio" id="" class="form-control" value="${data.precio}">
    
                    <label for="" class="form-label mt-2">Description</label>
                    <textarea name="descripcion" id="" class="form-control">${data.descripcion}</textarea>
    
                    <label for="" class="form-label mt-2">State</label>
                    <select name="estado" id="" class="form-select">
                        <option value="disponible" ${(data.estado === 'disponible'?'selected':'')}>Available</option>
                        <option value="ocupada" ${(data.estado === 'ocupada'?'selected':'')}>Not available</option>
                        <option value="mantenimiento" ${(data.estado === 'mantenimiento'?'selected':'')}>Maintenance</option>
                    </select>
    
                    <label for="" class="form-label mt-2">Door key card ID</label>
                    <input type="number" name="id_tarjeta_llave" id="" class="form-control" value="${data.id_tarjeta_llave}">
    
                    <button class="btn btn-warning my-3" type="submit">Update room</button>
                </form>
            `
            document.getElementById('respuesta').innerHTML = template
        })
}

function generarOptions(num){
    let template = ""
    for (let i = 1; i <= num; i++) {
        template += `
            <option value="${i}">Floor ${i}</option>
        `
    }
    let pisos = document.getElementById('pisos')
    pisos.innerHTML = template
}
