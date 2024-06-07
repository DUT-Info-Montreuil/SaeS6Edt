import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ImportFlopedtComponent } from './import-flopedt.component';

describe('ImportFlopedtComponent', () => {
  let component: ImportFlopedtComponent;
  let fixture: ComponentFixture<ImportFlopedtComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ImportFlopedtComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ImportFlopedtComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
