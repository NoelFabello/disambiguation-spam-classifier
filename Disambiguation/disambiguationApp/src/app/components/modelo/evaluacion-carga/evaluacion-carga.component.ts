import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { ApiService } from 'src/app/python-api.service';

@Component({
  selector: 'evaluacion-carga',
  templateUrl: './evaluacion-carga.component.html',
  styleUrls: ['./evaluacion-carga.component.scss']
})

export class EvaluacionCargaComponent implements OnInit{

  formEvaluacion : FormGroup = this.formBuilder.group({})
  formConfEvaluacion : FormGroup = this.formBuilder.group({})
  evaluacionLista: boolean = false;
  procesandoEvaluacion: boolean = false;
  mensajesError = {
    formulario : [{tipo: 'form', mensaje: 'Complete el formulario'}],
    nombreFichero : [{tipo: 'required', mensaje: 'El nombre del fichero de datos es requerido'}],
    tasaEvaluacion : [{tipo:'required' , mensaje: 'El porcentaje de evaluacion debe estar entre 1 y 100'}]
  }
  formIncompleto: boolean = false;
  exception: boolean = false;

  constructor(private formBuilder: FormBuilder, private readonly apiService: ApiService, private readonly routes: Router) {
  }

  ngOnInit(): void {
    this.formEvaluacion = this.formBuilder.group({
      exactitud : ['', []],
      precision : ['', []],
      recall : ['', []],
      f1 : ['', []],
      tcr1 : ['', []],
      tcr9 : ['', []],
      tcr999 : ['', []],
      imgcm : ['', []],
      imgroc : ['', []]
    });
    this.formConfEvaluacion = this.formBuilder.group({
      ficheroEvaluar : ['', [Validators.required]],
      tasaEvaluacion : ['', [Validators.required, Validators.pattern("^[0-9]*$"), Validators.min(1), Validators.max(100)]]
    });
    this.formConfEvaluacion.patchValue({tasaEvaluacion: 25})
    this.evaluacionLista = false
    this.formConfEvaluacion.get('ficheroEvaluar')?.disable()
  }

  evaluar() {
    this.formConfEvaluacion.get('ficheroEvaluar')?.enable()
    if (this.formConfEvaluacion.valid) {
      this.exception = false
      this.formIncompleto = false;
      this.procesandoEvaluacion = true;
      this.evaluacionLista = false;
      this.apiService.evaluarModeloFichero(this.formConfEvaluacion.value,'webImage').subscribe(
        data => {
          if(data.error == false){
            this.procesandoEvaluacion = false;
            this.evaluacionLista = true;
              this.formEvaluacion.patchValue({
                exactitud : data.message.exactitud,
                precision : data.message.precision,
                recall : data.message.recall,
                f1 : data.message.f1,
                tcr1 : data.message.tcr1,
                tcr9 : data.message.tcr9,
                tcr999 : data.message.tcr999,
                imgcm : data.message.imgcm,
                imgroc : data.message.imgroc
              });
            } else {
            this.procesandoEvaluacion = false;
            this.exception = true
            }
          }
          )
        } else {
          this.formIncompleto = true;
        }
      this.formConfEvaluacion.get('ficheroEvaluar')?.disable()
  }

  navegarEntrenar () {
    this.routes.navigate(['/modelo/entrenamiento'])
  }

  actualizarTasa(event : any){
    this.formConfEvaluacion.patchValue({tasaEvaluacion: event.target.value})
  }

  obtenerRuta(){
    this.apiService.obtenerRuta().subscribe(
      data => {
        this.formConfEvaluacion.patchValue({ficheroEvaluar: data})
      }
    )
  }
}
