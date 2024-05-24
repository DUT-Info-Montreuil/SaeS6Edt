import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AddModalEleveComponent } from './add-modal-eleve.component';

describe('AddModalEleveComponent', () => {
  let component: AddModalEleveComponent;
  let fixture: ComponentFixture<AddModalEleveComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [AddModalEleveComponent]
    });
    fixture = TestBed.createComponent(AddModalEleveComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
