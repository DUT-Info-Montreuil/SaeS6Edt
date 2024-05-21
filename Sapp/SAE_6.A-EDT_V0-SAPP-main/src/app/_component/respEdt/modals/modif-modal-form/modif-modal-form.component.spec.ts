import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ModifModalFormComponent } from './modif-modal-form.component';

describe('ModifModalFormComponent', () => {
  let component: ModifModalFormComponent;
  let fixture: ComponentFixture<ModifModalFormComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [ModifModalFormComponent]
    });
    fixture = TestBed.createComponent(ModifModalFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
