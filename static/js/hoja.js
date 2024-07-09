//----------------------------------------------------//
// 1- DECLARO VARIABLES PARA GUARDAR LOS DATOS DE CADA ID

const nombre = document.getElementById("nombre");
const apellido = document.getElementById("apellido");
const email = document.getElementById("email");
const tel = document.getElementById("telefono");
const consulta = document.getElementById("select");
const mensaje = document.getElementById("mensaje");
const form = document.getElementById("form");
const parrafo = document.getElementById("warnings");

// 2- CREO FUNCION CON ADD EVENT LISTENER PARA QUE CAPTE LAS ACCIONES DEL SUBMIT.

form. addEventListener ('submit', e=> {
//-> tiene 2 parametros: submit (el click en el boton enviar) y la funcion de cada input    
     e.preventDefault();
//-> pongo prevent.Default para que no se envíe el formulario de forma automática.

     let warnings = "" //se crea vacío para que vaya almacenando valor

     let entrar = false 

     let regexEmail = /^(([^<>()\[\]\.,;:\s@\”]+(\.[^<>() \[\]\.,;:\s@\”]+)*)|(\”.+\”))@(([^<>()[\]\.,;:\s@\ ”]+\.)+[^<>()[\]\.,;:\s@\”]{2,3})$/  //se utiliza la expresion regular para validar que tenga un @ y que tenga texto y . hasta 3 letras posteriores

     parrafo.innerHTML = "" //para que se limpie y aparezca un msj ultimo.

     //valida nombre:
    if(nombre.value.length == " "){
        alert(' Debe ingresar su Nombre !!!')
       // warnings +=   `El nombre es demasiado corto!!!! <br>`
        entrar = true    
    }

    //valida apellido:
    if(apellido.value.length == " "){
        alert(' Debe ingresar su Apellido!!!')
        entrar = true
    }

     //valida mail:
    if (!regexEmail.test(email.value)){
       alert('El Mail no es Válido!!')
       // warnings +=   `El mail no es válido! <br>`
        entrar = true
    }

    //valida teléfono FALTA!!!!!!
    // if (!Number.isInteger (tel.value)){
    //     alert ('Debe completar el Teléfono con  SÓLO NÚMEROS!')
    //     entrar = true
    // }

    //valida el select
    if (consulta.value == " "){
        alert('Debe Elegir una Opción para su consulta!');
        entrar = true
    }

    // //valida mensaje FALTA!!!!!
    // if (mensaje.value < minleght){
    //     alert('El Campo Mensaje está vacío!')
    //     entrar = true
    // }


    if (entrar) {
        alert ('COMPLETE DE MANERA CORRECTA POR FAVOR!!')
       // parrafo.innerHTML = warnings
    } else{
        alert ('ENVIADO CORRECTAMENTE!!!')
        //parrafo.innerHTML = "Enviado!!"
    }



})

