import { Injectable } from '@angular/core';
import { from, map, Observable, retry, Subject } from 'rxjs';

declare global {
  interface Window {
    pywebview: {
      pywebviewready: any;
      api: {
        Preprocesar(): any
      };
    };
  }
}

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  private isWebViewReady = false;

  private isWVReady = new Subject<boolean>();
  public isWVReady$ = this.isWVReady.asObservable();

  api: any;

  setApi(value: boolean, api: any): void {
    this.api = api;
    this.isWebViewReady = value;
    this.isWVReady.next(value);
  }

  Preprocesar(formData:any) : Observable<any> {
    var method = formData.metodo
    var file = formData.ficheroEntrada
    var level = 0
    if (method === 'tokenize') {
      level = formData.caracteristicas
    } else {
      level = formData.profundidad
    }
    var outputFile = formData.ficheroSalida
    var outputBinaryTableFile = formData.ficheroSalidaMatriz

    return from(this.api.preProcess(method, file, level, outputFile, outputBinaryTableFile))
  }

  entrenarModelo(formData:any) : Observable<any> {
    var file = formData.ficheroEntrenar
    var model = formData.modelo
    var trainRate = formData.tasaEntrenamiento
    var cv = formData.pliegues
    return from(this.api.train(file, model, trainRate, cv))
  }

  evaluarModelo(outputImage : string) : Observable<any> {
    return from(this.api.evaluate(outputImage))
  }

  desambiguar(formData : any) : Observable<any> {
    return from(this.api.desambiguar(formData.textoDesambiguar, formData.metodo))
  }

  evaluarModeloFichero(formData:any, outputImage : string) : Observable<any> {
    return from(this.api.evaluateFile(formData.ficheroEvaluar, formData.tasaEvaluacion,outputImage))
  }

  cargarModelo(formData:any) : Observable<any> {
    return from(this.api.cargarModelo(formData.ficheroCarga));
  }

  guardarModelo(formData:any) : Observable<any> {
    return from(this.api.guardarModelo(formData.nombreGuardarModelo));
  }

  obtenerRuta() : Observable<any> {
    return from(this.api.obtainFile());
  }

  comprobarModelo() : Observable<any> {
    return from(this.api.getModelCheck())
  }

  Close() {
    this.api.closeWindow()
  }


}
