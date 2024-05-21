import { Component, Inject } from '@angular/core';
import {MAT_DIALOG_DATA} from '@angular/material/dialog';
import { ToastrService } from 'ngx-toastr';
import { Group } from 'src/app/_model/entity/group.model';
import { UserGroupService } from 'src/app/_service/user_group.service';

@Component({
  selector: 'app-modif-modal-group',
  templateUrl: './modif-modal-group.component.html',
  styleUrls: ['./modif-modal-group.component.scss']
})
export class ModifModalGroupComponent {

  groupesKeys : Group[] = [];
  groupesValues : Group[][] = [];
  ancienGroupe : Group;
  nouveauGroupe : Group;
  eleve : any;
  confirmChange: boolean = false;

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: any,
    private userGroupService: UserGroupService,
    private toastr: ToastrService,
    ) {
  }

  ngOnInit(): void{
    this.groupesKeys = Array.from(this.data.groupes.keys());
    this.groupesValues = Array.from(this.data.groupes.values());
    this.ancienGroupe = this.data.ancienGroupe;
    this.eleve = this.data.eleve;
  }

  onClickGroupe(nouveauGroupe: Group){
    if (nouveauGroupe == this.ancienGroupe){
      this.toastr.warning(this.eleve.name + " " + this.eleve.lastname + " est déjà dans ce groupe");
    } else {
      this.confirmChange = !this.confirmChange;
      this.nouveauGroupe = nouveauGroupe;
    }
  }

  onClickConfirmChange(){
    this.userGroupService.modifyGroupStudent(this.eleve.id_student, this.nouveauGroupe.id, this.ancienGroupe.id).subscribe({
      next: response => {
        this.toastr.success(this.eleve.name + " " + this.eleve.lastname + " est maintenant dans le groupe " + this.nouveauGroupe.name);
        this.userGroupService.notifyUserGroupRefresh();
      },
      error: error=> {
        this.toastr.error("une erreur est survenue lors de la modification du groupe");
        console.log(error);
      }
    });
  }
}
