import { Component, OnInit } from '@angular/core';
import { AbstractControl, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ApiService } from 'src/app/python-api.service';


@Component({
  selector: 'app-preprocesamiento',
  templateUrl: './preprocesamiento.component.html',
  styleUrls: ['./preprocesamiento.component.scss']
})
export class PreprocesamientoComponent implements OnInit{

  completado : boolean = false
  synsetMethod : boolean = true;
  preprocesando : boolean = false;
  formPreprocesamiento: FormGroup;
  formularioIncompleto: boolean = false;
  mensajesError = {
    formulario : [{tipo: 'form', mensaje: 'Complete el formulario'}, {tipo: 'current', mensaje: 'Ya hay un preprocesamiento en curso'}],
    ficheroEntrada: [{tipo: 'required', mensaje: 'El fichero de entrada de datos es requerido'}],
    ficheroSalida: [{tipo: 'required', mensaje: 'El nombre para el fichero de salida es requerido'}],
    ficheroSalidaMatriz: [{tipo: 'required', mensaje: 'El nombre para el fichero de salida de matriz es requerido'}],
    profundidad: [{tipo: 'valorMinimo', mensaje: 'El valor del campo debe ser vacío o mayor a 1'}],
    caracteristicas: [{tipo: 'valorMinimo', mensaje: 'El valor del campo debe ser vacío o mayor a 1'}]
   }
  exception: boolean = false;
  exceptionMessage: any = '';
  current: boolean = false;

  constructor(private formBuilder: FormBuilder, private readonly apiService: ApiService) {
    this.formPreprocesamiento = this.formBuilder.group({

    });
  }

  ngOnInit(): void {
    this.formPreprocesamiento = this.formBuilder.group({
      ficheroEntrada: ['', [Validators.required]],
      metodo: ['', []],
      profundidad: ['',[Validators.pattern("^[0-9]*$"), this.valorMinimo(1)]],
      caracteristicas: ['',[Validators.pattern("^[0-9]*$"), this.valorMinimo(1)]],
      ficheroSalida: ['', [Validators.required]],
      ficheroSalidaMatriz: ['', [Validators.required]]
    });
    this.formPreprocesamiento.patchValue({ metodo: 'father' });
    this.formPreprocesamiento.get('ficheroEntrada')?.disable()
  }

  proponerNombre(event:any) {
    var matrizNombre = 'matriz-' + event.target.value
    this.formPreprocesamiento.patchValue({ficheroSalidaMatriz: matrizNombre})
  }

  onSelectChange(event:any) {
    if (event.target.value == "tokenize") {
      this.synsetMethod = false;
      this.formPreprocesamiento.patchValue({profundidad: null});
    } else {
      this.synsetMethod = true;
      this.formPreprocesamiento.patchValue({caracteristicas: null});
    }
  }

  valorMinimo(min: number) {
    return (control: AbstractControl) => {
      if (!control.value || control.value >= min) {
        return null;
      }
      return { min: true };
    };
  }

  obtenerRuta(){
    this.apiService.obtenerRuta().subscribe(
      data => {
        this.formPreprocesamiento.patchValue({ficheroEntrada: data})
      }
    )
  }

  Preprocesar(){
    this.formPreprocesamiento.get('ficheroEntrada')?.enable ()
    this.completado = false
    this.exception = false
    this.current = false
    this.preprocesando = false
    if (this.formPreprocesamiento.valid) {
      this.formularioIncompleto = false;
      this.preprocesando = true;
      this.apiService.Preprocesar(this.formPreprocesamiento.getRawValue()).subscribe(
        datos=> {
          if(datos.error == false){
            this.preprocesando = false;
            this.completado = true
            this.current = false
            } else {
            if(datos.code == 1) {
              this.current = true
            } else {
              this.preprocesando = false
              this.exception = true
            }
          }
        }
      )
    } else {
      this.formularioIncompleto = true
    }
    this.formPreprocesamiento.get('ficheroEntrada')?.disable()
  }
}
