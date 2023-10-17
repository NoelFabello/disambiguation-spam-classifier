import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EvaluacionCargaComponent } from './evaluacion-carga.component';

describe('EvaluacionCargaComponent', () => {
  let component: EvaluacionCargaComponent;
  let fixture: ComponentFixture<EvaluacionCargaComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [EvaluacionCargaComponent]
    });
    fixture = TestBed.createComponent(EvaluacionCargaComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
