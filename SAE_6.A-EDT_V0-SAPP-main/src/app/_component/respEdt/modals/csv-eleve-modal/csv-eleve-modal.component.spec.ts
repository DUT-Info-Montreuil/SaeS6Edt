import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CsvEleveModalComponent } from './csv-eleve-modal.component';

describe('CsvEleveModalComponent', () => {
  let component: CsvEleveModalComponent;
  let fixture: ComponentFixture<CsvEleveModalComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [CsvEleveModalComponent]
    });
    fixture = TestBed.createComponent(CsvEleveModalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
