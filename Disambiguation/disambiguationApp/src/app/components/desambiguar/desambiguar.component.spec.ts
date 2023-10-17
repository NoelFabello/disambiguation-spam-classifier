import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DesambiguarComponent } from './desambiguar.component';

describe('DesambiguarComponent', () => {
  let component: DesambiguarComponent;
  let fixture: ComponentFixture<DesambiguarComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [DesambiguarComponent]
    });
    fixture = TestBed.createComponent(DesambiguarComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
