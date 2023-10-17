import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { EntrenamientoComponent } from './components/modelo/entrenamiento/entrenamiento.component';
import { PreprocesamientoComponent } from './components/preprocesamiento/preprocesamiento.component';
import { EvaluacionComponent } from './components/modelo/evaluacion/evaluacion.component';
import { ModeloComponent } from './components/modelo/modelo.component';
import { EvaluacionCargaComponent } from './components/modelo/evaluacion-carga/evaluacion-carga.component';
import { DesambiguarComponent } from './components/desambiguar/desambiguar.component';

const routes: Routes = [
  { path: '', redirectTo: 'desambiguar', pathMatch: 'full' },
  { path: 'preprocesamiento', component: PreprocesamientoComponent },
  { path: 'desambiguar', component: DesambiguarComponent },
  {
    path: "modelo", component: ModeloComponent,
    children: [
      { path: '', redirectTo: 'entrenamiento', pathMatch: 'full' },
      { path: "entrenamiento", component: EntrenamientoComponent},
      { path: "evaluacion", component: EvaluacionComponent},
      { path: "evaluacion-carga", component: EvaluacionCargaComponent},
      { path: '**', redirectTo: 'entrenamiento' }
    ]
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
