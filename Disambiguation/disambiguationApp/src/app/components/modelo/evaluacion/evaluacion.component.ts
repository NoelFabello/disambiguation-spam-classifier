import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { ApiService } from 'src/app/python-api.service';

@Component({
  selector: 'evaluacion',
  templateUrl: './evaluacion.component.html',
  styleUrls: ['./evaluacion.component.scss']
})
export class EvaluacionComponent implements OnInit{

  formEvaluacion : FormGroup = this.formBuilder.group({})
  evaluacionLista: boolean = false;
  procesandoEvaluacion: boolean = false;
  formGuardarModelo: FormGroup = this.formBuilder.group({});
  modeloGuardado: boolean = false;

  mensajesError = {
    nombreGuardarModelo : [{tipo: 'required', mensaje: 'El nombre del modelo es requerido'}]
  }
  exception: boolean = false;
  exceptionGuardar: boolean = false;

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
    this.formGuardarModelo = this.formBuilder.group({
      nombreGuardarModelo : ['', [Validators.required]]
    });
    this.evaluacionLista = false
  }

  evaluar() {
    this.procesandoEvaluacion = true
    this.modeloGuardado = false
    this.evaluacionLista = false
    this.exception = false;
    this.apiService.evaluarModelo('webImage').subscribe(
      data => {
        if(!data.error){
          console.log(data)
          this.procesandoEvaluacion = false
          this.evaluacionLista = true
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
            })
        }else {
          this.procesandoEvaluacion = false
          this.exception = true
        }
      }
    )
  }

  navegarEntrenar () {
    this.routes.navigate(['/modelo/entrenamiento'])
  }

  guardarModelo() {
    if(this.formGuardarModelo.valid){
      this.modeloGuardado = false
      this.exceptionGuardar = false
      this.apiService.guardarModelo(this.formGuardarModelo.value).subscribe(
        data => {
          if(data.error ==false){
            this.modeloGuardado = true
          } else {
            this.exceptionGuardar = true
          }
          });
    }
  }


}
