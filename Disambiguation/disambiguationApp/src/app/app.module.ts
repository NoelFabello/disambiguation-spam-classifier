import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { PreprocesamientoComponent } from './components/preprocesamiento/preprocesamiento.component';
import { EntrenamientoComponent } from './components/modelo/entrenamiento/entrenamiento.component';
import { EvaluacionComponent } from './components/modelo/evaluacion/evaluacion.component';
import { ModeloComponent } from './components/modelo/modelo.component';
import { EvaluacionCargaComponent } from './components/modelo/evaluacion-carga/evaluacion-carga.component';
import { ReactiveFormsModule, FormsModule } from '@angular/forms';
import { DesambiguarComponent } from './components/desambiguar/desambiguar.component';

@NgModule({
  declarations: [
    AppComponent,
    PreprocesamientoComponent,
    EntrenamientoComponent,
    EvaluacionComponent,
    ModeloComponent,
    EvaluacionCargaComponent,
    DesambiguarComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    ReactiveFormsModule,
    FormsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
