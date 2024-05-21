import { Component, Inject, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import {MAT_DIALOG_DATA} from '@angular/material/dialog';
import { ToastrService } from 'ngx-toastr';
import { Observable, tap, catchError, finalize } from 'rxjs';
import { Group } from 'src/app/_model/entity/group.model';
import { Student } from 'src/app/_model/entity/student.model';
import { StudentService } from 'src/app/_service/student.service';
import { UserGroupService } from 'src/app/_service/user_group.service';

@Component({
  selector: 'app-add-modal-eleve',
  templateUrl: './add-modal-eleve.component.html',
  styleUrls: ['./add-modal-eleve.component.scss']
})
export class AddModalEleveComponent implements OnInit{

  eleve: Student;
  groupeSelectionne: Group | null = null;
  groupesKeys : Group[] = [];
  groupesValues : Group[][] = [];

  formAddEleve = new FormGroup({
    lastname: new FormControl("", Validators.required),
    name: new FormControl("", Validators.required),
    INE: new FormControl("", Validators.required),
    username: new FormControl("", Validators.required),
    password: new FormControl("", Validators.required),
  });

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: any,
    private studentService: StudentService,
    private userGroupService: UserGroupService,
    private toastr: ToastrService
  ) { }

  ngOnInit(): void {
    this.groupesKeys = Array.from(this.data.groupes.keys());
    this.groupesValues = Array.from(this.data.groupes.values());
  }

  onClickGroupe(groupe: Group) {
    this.groupeSelectionne = groupe;
  }

  onSubmitAddEleve(): Observable<any> {
    if (this.formAddEleve.valid) {
      let INE = parseInt(this.formAddEleve.value.INE!, 10);
      let name = this.formAddEleve.value.name!;
      let lastname = this.formAddEleve.value.lastname!;
      let username = this.formAddEleve.value.username!;
      let password = this.formAddEleve.value.password!;
      this.eleve = new Student(0, INE, name, lastname, username, password);
  
      return this.studentService.addStudent(this.eleve).pipe(
        tap(response => {
          this.eleve = response;
        }),
        catchError(error => {
          this.toastr.error("Une erreur est survenue lors de l'ajout de l'élève");
          console.log(error);
          throw error;
        }),
        finalize(() => {
          this.formAddEleve.reset();
        })
      );
    } else {
      this.toastr.error('Veuillez remplir correctement tous les champs du formulaire.');
      return new Observable();
    }
  }

  linkStudentToGroup() {
    if (this.groupeSelectionne != null){
      this.userGroupService.addStudentToGroup(this.eleve.id, this.groupeSelectionne.id).subscribe({
        next: responde => {
          this.userGroupService.notifyUserGroupRefresh();
          this.toastr.success("l'élément a bien été ajouté");
        },
        error: error => {
          this.toastr.error("Une erreur est survenue lors de l'ajout de l'élève au groupe");
          console.log(error);
        }
      });
    } else {
      this.toastr.error("Veuillez selectionner un groupe");
    }
  }

  ajouterEleveEtGroupe() {
    try {
      this.onSubmitAddEleve().subscribe({
        next: response => {
          this.linkStudentToGroup();
        }
      });
    } catch (error) {
      this.toastr.error("Une erreur est survenue");
      console.log(error);
    }
  }

}
