import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ApiService } from 'src/app/python-api.service';

@Component({
  selector: 'app-desambiguar',
  templateUrl: './desambiguar.component.html',
  styleUrls: ['./desambiguar.component.scss']
})
export class DesambiguarComponent {

  formDesambiguar : FormGroup = this.formBuilder.group({})
  desambiguacionLista: boolean = false;
  procesandoDesambiguacion: boolean = false;
  acepciones : any = [];
  words: any = [];
  definitions: any = [];

  mensajesError = {
    formulario : [{tipo: 'form', mensaje: 'Complete el formulario'}],
    textoDesambiguar : [{tipo: 'required', mensaje: 'Debe haber contenido en el texto para desambiguar'}]
  }
  formIncompleto: boolean = false;
  exception: boolean = false;

  constructor(private formBuilder: FormBuilder, private readonly apiService: ApiService) {
  }

  ngOnInit(): void {
    this.formDesambiguar = this.formBuilder.group({
      metodo : ['', []],
      textoDesambiguar : ['', [Validators.required]]
    });
    this.words = [];
    this.formDesambiguar.patchValue({metodo : 'father'})
    this.desambiguacionLista = false
    this.procesandoDesambiguacion = false;
}

  desambiguar() : void{
    this.exception = false
    this.desambiguacionLista = false
    if(this.formDesambiguar.valid){
      this.formIncompleto = false
      this.procesandoDesambiguacion = true
      this.apiService.desambiguar(this.formDesambiguar.value).subscribe(
        data=>{
          this.procesandoDesambiguacion = false
          if(!data.error){
            this.desambiguacionLista = true
            this.acepciones = data.message.synsets;
            this.definitions = data.message.definitions;
            this.words = data.message.words;
            this.procesandoDesambiguacion = false
          } else {
            this.exception = true
          }
        }
      )
    } else {
      this.formIncompleto = true
    }
  }

  getDiccionarioKeys(): string[] {
    return Object.keys(this.acepciones);
  }

}

