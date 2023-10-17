import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { ApiService } from 'src/app/python-api.service';

@Component({
  selector: 'entrenamiento',
  templateUrl: './entrenamiento.component.html',
  styleUrls: ['./entrenamiento.component.scss']
})
export class EntrenamientoComponent implements OnInit{

  formEntrenamiento: FormGroup = this.formBuilder.group({});
  exception: boolean = false;
  mensajesError = {
    formulario : [{tipo: 'form', mensaje: 'Complete el formulario'}],
    ficheroEntrenar: [{tipo: 'required', mensaje: 'El fichero para el entrenamiento del modelo es requerido'}],
    ficheroCarga: [{tipo: 'required', mensaje: 'El fichero para el cargar el modelo es requerido'}],
    tasaEntrenamietno: [{tipo: 'any', mensaje: 'El valor de la tasa de entrenamiento debe estar entre 5 y 95'}],
    pliegues: [{tipo: 'any', mensaje: 'El valor de los pliegues debe ser mayor a 1'}]
  }

  formCarga : FormGroup = this.formBuilder.group({});
  completadoEntrenamiento: boolean = false;
  formularioIncompletoEntrenamiento: boolean = false;
  preprocesandoEntrenamiento: boolean = false;
  formularioIncompletoCarga: boolean = false;
  completadoCarga: boolean = false;
  preprocesandoCarga: boolean = false;
  modeloPrecargado: boolean = false;
  exceptionCarga: boolean = false;

  constructor(private formBuilder: FormBuilder, private readonly apiService: ApiService, private readonly routes: Router) {
  }

  ngOnInit(): void {
    this.formEntrenamiento = this.formBuilder.group({
      ficheroEntrenar : ['', [Validators.required]],
      modelo : ['', []],
      tasaEntrenamiento : ['', [Validators.required, Validators.pattern("^[0-9]*$"), Validators.min(5), Validators.max(95)]],
      pliegues : ['', [Validators.required, Validators.pattern("^[0-9]*$"), Validators.min(2)]]
    });
    this.formEntrenamiento.patchValue({tasaEntrenamiento: 75, pliegues: 10, modelo: 'Gaussian'})
    this.formCarga = this.formBuilder.group({
      ficheroCarga : ['', [Validators.required]]
    });
    this.formEntrenamiento.get('ficheroEntrenar')?.disable()
    this.formCarga.get('ficheroCarga')?.disable()
    this.comprobarModelo()
  }


  obtenerRuta(componente : string){
    this.apiService.obtenerRuta().subscribe(
      data => {
        if(componente === 'ficheroEntrenar'){
          this.formEntrenamiento.patchValue({ficheroEntrenar: data})
        } else if (componente === 'ficheroCarga'){
          this.formCarga.patchValue({ficheroCarga: data})
        }
      }
    )
  }

  entrenarModelo() {
    this.formCarga.get('ficheroEntrenar')?.disable()
    this.completadoEntrenamiento = false
    this.exception = false
    if (this.formEntrenamiento.valid) {
      this.formularioIncompletoEntrenamiento = false;
      this.preprocesandoEntrenamiento = true;
      this.apiService.entrenarModelo(this.formEntrenamiento.getRawValue()).subscribe(
        datos=> {
          if(!datos.error){
            this.preprocesandoEntrenamiento = false;
            this.completadoEntrenamiento = true
            this.completadoCarga = false
          } else {
            this.exception = true
            this.preprocesandoEntrenamiento = false;
          }
        }
      )
    } else {
      this.formularioIncompletoEntrenamiento = true
    }
    this.formCarga.get('ficheroEntrenar')?.enable()
  }

  cargarModelo() {
    this.formCarga.get('ficheroCarga')?.enable()
    this.completadoCarga = false
    this.exceptionCarga = false
    if (this.formCarga.valid) {
      this.formularioIncompletoCarga = false;
      this.preprocesandoCarga = true;
      this.apiService.cargarModelo(this.formCarga.getRawValue()).subscribe(
        datos=> {
          if (!datos.error){
            this.preprocesandoCarga = false;
            this.completadoCarga = true
            this.completadoEntrenamiento = false
          } else {
            this.completadoCarga = false
            this.preprocesandoCarga = false;
            this.exceptionCarga = true
          }

        }
      )
    } else {
      this.formularioIncompletoCarga = true
    }
    this.formCarga.get('ficheroCarga')?.disable()
  }

  actualizarTasa(event : any){
    this.formEntrenamiento.patchValue({tasaEntrenamiento: event.target.value})
  }

  actualizarPliegues(event : any){
    this.formEntrenamiento.patchValue({pliegues: event.target.value})
  }

  evaluarModeloEntrenado(){
    this.routes.navigate(['/modelo/evaluacion'])
  }

  evaluarModeloCargado(){
    this.routes.navigate(['/modelo/evaluacion-carga'])
  }

  comprobarModelo() {
    this.apiService.comprobarModelo().subscribe(
      data=>{
        if(!data.error && data.message){
          this.modeloPrecargado = true
        } else {
          this.modeloPrecargado = false
        }
      }
    )
  }

}
