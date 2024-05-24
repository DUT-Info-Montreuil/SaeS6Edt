import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AddModalPromoComponent } from './add-modal-promo.component';

describe('AddModalPromoComponent', () => {
  let component: AddModalPromoComponent;
  let fixture: ComponentFixture<AddModalPromoComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [AddModalPromoComponent]
    });
    fixture = TestBed.createComponent(AddModalPromoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
