import { Component, EventEmitter, Input, Output } from '@angular/core';


@Component({
  selector: 'app-import-flopedt',
  standalone: true,
  imports: [],
  templateUrl: './import-flopedt.component.html',
  styleUrls: ['./import-flopedt.component.scss']
})
export class ImportFlopedtComponent {

  @Output() closeModal: EventEmitter<void> = new EventEmitter<void>();


  /*
    @function closeModaleAdd
    @desc: close modal
   */
  closeModaleAdd() {
      this.closeModal.emit();
  }
}
