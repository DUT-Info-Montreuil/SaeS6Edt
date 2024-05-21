import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ModifModalGroupComponent } from './modif-modal-group.component';

describe('ModifModalGroupComponent', () => {
  let component: ModifModalGroupComponent;
  let fixture: ComponentFixture<ModifModalGroupComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [ModifModalGroupComponent]
    });
    fixture = TestBed.createComponent(ModifModalGroupComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
