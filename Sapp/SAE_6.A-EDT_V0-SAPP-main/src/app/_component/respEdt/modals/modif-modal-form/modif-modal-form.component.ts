import { Component, OnInit} from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import {MAT_DIALOG_DATA} from '@angular/material/dialog';
import { Inject } from '@angular/core';
import { ToastrService } from 'ngx-toastr';
import { TeacherService } from 'src/app/_service/teacher.service';
import { Teacher } from 'src/app/_model/entity/teacher.model';
import { __values } from 'tslib';
import { RoomService } from 'src/app/_service/room.service';
import { Room } from 'src/app/_model/entity/room.model';
import { ResourceService } from 'src/app/_service/resource.service';
import { Resource } from 'src/app/_model/entity/resource.model';
import { StudentService } from 'src/app/_service/student.service';
import { Student } from 'src/app/_model/entity/student.model';
import { EdtManager } from 'src/app/_model/entity/edtManager.model';
import { EdtManagerService } from 'src/app/_service/edtManager.service';
import { AffiliationRespEdtService } from 'src/app/_service/affiliationRespEdt.service';
import { FormsComponent } from '../../forms/forms.component';

@Component({
  selector: 'app-modif-modal-form',
  templateUrl: './modif-modal-form.component.html',
  styleUrls: ['./modif-modal-form.component.scss']
})
export class ModifModalFormComponent implements OnInit{

  teacher:Teacher;
  responsable : EdtManager;
  salle:Room = new Room();
  ressource:Resource = new Resource();
  eleve:Student;

  searchText: any;


  promos = this.formsComponent.promos;
  elementName: any = null;

  public formSelectionne: any = null;

  formModifSalle = new FormGroup({
    name : new FormControl("", Validators.required),
    ordi: new FormControl("", Validators.required),
    videoProjecteur: new FormControl("", Validators.required),
    tableauNumerique: new FormControl("", Validators.required)
  })

  formModifProfesseur = new FormGroup({
    id: new FormControl<number|null>(null),
    name: new FormControl("", Validators.required),
    lastname: new FormControl("", Validators.required)
  })

  formModifResponsable = new FormGroup({
    id: new FormControl<number|null>(null),
    name: new FormControl("", Validators.required),
    lastname: new FormControl("", Validators.required)
  })

  formModifStudent = new FormGroup({
    id: new FormControl<number|null>(null),
    name: new FormControl("", Validators.required),
    lastname: new FormControl("", Validators.required)
  })

  formModifRessource = new FormGroup({
    name: new FormControl("", Validators.required),
    initial: new FormControl("", Validators.required),
    id_promo: new FormControl("", Validators.required)
  })

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: any,
    private teacherService: TeacherService,
    private responsableService: EdtManagerService,
    private roomService: RoomService,
    private ressourceService: ResourceService,
    private studentService: StudentService,
    private toastr: ToastrService,
    private formsComponent: FormsComponent,
    private affiliationService: AffiliationRespEdtService
    ){
  }

  responsablesChanged() {
    this.responsableService.notifyRespRefresh();
  }

  sallesChanged() {
    this.roomService.notifySalleRefresh();
  }

  profsChanged() {
    this.teacherService.notifyProfRefresh();
  }

  ressourceChanged(){
    this.ressourceService.notifyRessourceRefresh();
  }

  elevesChanged(){
    this.studentService.notifyStudentRefresh();
  }

  ngOnInit(): void{
    this.promos = this.data.promos;
    this.formSelectionne = this.data.formSelectionne;
    switch (this.formSelectionne) {
      case "formSalle":
        this.elementName = this.data.element.name;
        this.setSalleValues();
        break;
      case "formProfesseur":
        this.elementName = this.data.element.staff.user.name + " " + this.data.element.staff.user.lastname;
        this.setProfValues();
        break;
      case "formRessource":
        this.elementName = this.data.element.initial;
        this.setRessourceValues();
        break;
      case "formEleve":
        this.elementName = this.data.element.user.name + " " + this.data.element.user.lastname;
        this.setEleveValues();
        break;
      case "formResponsable":
        this.elementName = this.data.element.staff.user.name + " " + this.data.element.staff.user.lastname;
        this.setResponsableValues();
        break;
    }
    
  }

  getElementId(): number{
    return this.data.element.id;
  }

  setResponsableValues(){
    this.formModifResponsable.patchValue({
      id: this.getElementId(),
      name: this.data.element.staff.user.name,
      lastname: this.data.element.staff.user.lastname
    });
  }

  setProfValues(){
    this.formModifProfesseur.patchValue({
      id: this.getElementId(),
      name: this.data.element.staff.user.name,
      lastname: this.data.element.staff.user.lastname,
    });
  }

  setEleveValues(){
    this.formModifStudent.patchValue({
      id: this.getElementId(),
      name: this.data.element.user.name,
      lastname: this.data.element.user.lastname,
    });
  }

  setSalleValues(){
    this.formModifSalle.patchValue({
      name: this.data.element.nom,
      ordi: this.data.element.ordi,
      videoProjecteur: this.data.element.videoProjecteur,
      tableauNumerique: this.data.element.tableauNumerique
    });
  }

  setRessourceValues(){
    this.formModifRessource.patchValue({
      name: this.data.element.name,
      initial: this.data.element.initial,
      id_promo: this.data.element.id_promo
    })
  }

  onSubmitModifSalle(){
    if (this.formModifSalle.valid){
      this.salle = Object.assign(this.salle, this.formModifSalle.value);
      this.roomService.updateSalle(this.salle).subscribe({
        next: response => {
          this.toastr.success("la salle a bien été modifiée !");
          this.sallesChanged();
        },
        error: error=> {this.toastr.error("erreur");}
      });
    } else {
      this.toastr.error('Veuillez remplir correctement tous les champs du formulaire.');
    }
  }

  onSubmitModifProfesseur(){
    if (this.formModifProfesseur.valid){
      let id = this.data.element.id;
      let name = this.formModifProfesseur.value.name!;
      let lastname = this.formModifProfesseur.value.lastname!;
      let username = this.data.element.staff.user.username;
      let password = this.data.element.staff.user.password;
      this.teacher = new Teacher(id, name, lastname, username, password, this.data.prof_activated);
      this.teacherService.updateTeacher(this.teacher).subscribe({
        next: response => {
          this.toastr.success("le professeur a bien été modifié !");
          this.profsChanged();
        },
        error: error=> {this.toastr.error("erreur");}
      });
    } else {
      this.toastr.error('Veuillez remplir correctement tous les champs du formulaire.');
    }
  }

  onSubmitModifResponsable(){
    if (this.formModifResponsable.valid){
      let id = this.data.element.id;
      let name = this.formModifResponsable.value.name!;
      let lastname = this.formModifResponsable.value.lastname!;
      let username = this.data.element.staff.user.username;
      let password = this.data.element.staff.user.password;
      this.responsable = new EdtManager(id, name, lastname, username, password);
      this.responsableService.updateEdtManager(this.responsable).subscribe({
        next: response => {
          this.toastr.success("le responsable a bien été modifié !");
          this.responsablesChanged();
        },
        error: error=> {this.toastr.error("erreur");}
      });
    } else {
      this.toastr.error('Veuillez remplir correctement tous les champs du formulaire.');
    }
  }

  onSubmitModifRessource(){
    if (this.formModifRessource.valid){
      this.ressource = Object.assign(this.ressource, this.formModifRessource.value);
      this.ressourceService.updateResource(this.ressource).subscribe({
        next:reponse => {
          this.toastr.success("la ressource a bien été modifié !");
          this.ressourceChanged();
        },
        error: error=> {this.toastr.error("erreur");}
      });
    } else {
      this.toastr.error('Veuillez remplir correctement tous les champs du formulaire.');
    }
  }

  onSubmitModifEleve(){
    if (this.formModifStudent.valid){
      let id = this.getElementId();
      let INE = this.data.element.INE;
      let name = this.formModifStudent.value.name!;
      let lastname = this.formModifStudent.value.lastname!;
      let username = this.data.element.username;
      let password = this.data.element.password;
      this.eleve = new Student(id, INE, name, lastname, username, password);
      this.studentService.updateStudent(this.eleve).subscribe({
        next: response => {
          this.toastr.success("le professeur a bien été modifié !");
          this.elevesChanged();
        },
        error: error=> {this.toastr.error("erreur");}
      });
    } else {
      this.toastr.error('Veuillez remplir correctement tous les champs du formulaire.');
    }
  }

  addAffiliation(resp: EdtManager){
    this.affiliationService.affiliateRespEdtToPromo(resp.id,this.data.element.promo.id).subscribe({
      next: response => {
        this.toastr.success("le responsable a bien été ajouté !");
        location.reload();
      },
      error: error=> {this.toastr.error("erreur");}
    });
  }
}
