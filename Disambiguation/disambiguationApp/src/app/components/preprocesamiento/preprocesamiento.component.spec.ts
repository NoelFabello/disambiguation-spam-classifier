import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PreprocesamientoComponent } from './preprocesamiento.component';

describe('PreprocesamientoComponent', () => {
  let component: PreprocesamientoComponent;
  let fixture: ComponentFixture<PreprocesamientoComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [PreprocesamientoComponent]
    });
    fixture = TestBed.createComponent(PreprocesamientoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
