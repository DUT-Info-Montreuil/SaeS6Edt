import { Component, OnInit, Inject } from '@angular/core';
import { FormControl, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { MAT_DIALOG_DATA } from '@angular/material/dialog';
import { ToastrService } from 'ngx-toastr';
import { AuthService } from 'src/app/_security/auth.service';
import { UserService } from 'src/app/_service/user.service';

@Component({
  selector: 'app-change-passwd',
  templateUrl: './change-passwd.component.html',
  styleUrls: ['./change-passwd.component.scss']
})
export class ChangePasswdComponent implements OnInit{

  username: string;
  password: string;

  goodOldPass: boolean = true;
  goodNewPass: boolean = true; 
  goodRptNewPass: boolean = true;

  formChangePasswd = new FormGroup({
    oldPasswd: new FormControl("", Validators.required),
    newPasswd: new FormControl("", Validators.required),
    rptNewPasswd: new FormControl("", Validators.required)
  });

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: any,
    private authService: AuthService,
    private userService: UserService,
    private toastr: ToastrService,
  ){}

  ngOnInit(): void {
    this.password = "password"
    this.userService.getIdentify().subscribe({
      next: user => {
        this.username = user.username;
      },
      error: error => {}
    })
  }

  onEnterOld(event: any) {
    this.checkPasswd(this.username, event.target.value);
  }

  onEnterNew(){
    if (this.formChangePasswd.value.oldPasswd! == this.formChangePasswd.value.newPasswd!){
      this.goodNewPass = false;
    } else {
      this.goodNewPass = true;
    }
  }

  onEnterRepeat(){
    if (this.formChangePasswd.value.newPasswd! != this.formChangePasswd.value.rptNewPasswd!){
      this.goodRptNewPass = false;
    } else {
      this.goodRptNewPass = true;
    }
  }

  onSubmit(){
    if (this.allGood()){
      let oldPasswd = this.formChangePasswd.value.oldPasswd!;
      let newPasswd = this.formChangePasswd.value.newPasswd!;
      this.authService.changePasswd(this.username, oldPasswd, newPasswd).subscribe({
        next: response => {
          this.toastr.success("le mot de passe à bien été changé !");
          this.formChangePasswd.reset();
        },
        error: error => {
          this.toastr.error("une erreur est survenue lors du changement de mot de passe !");
        }
      });
    }
  }

  checkPasswd(username: string, password: string) {
    this.authService.verifyPasswd(username, password).subscribe({
      next: response => {
        this.goodOldPass = true;
      },
      error: error =>{
        console.warn("acien mot de passe incorrecte !");
        this.goodOldPass = false;
      }
    });
  }

  hasRequiredLenght(): boolean{
    return this.formChangePasswd.value.newPasswd!.length >= 12;
  }

  hasNumber(): boolean {
    return /\d/.test(this.formChangePasswd.value.newPasswd!);
  }

  hasSpecialCharacter(): boolean {
    return /[!@#$%^&*(),.?":{}|<>]/.test(this.formChangePasswd.value.newPasswd!);
  }

  hasUppercase(): boolean {
    return /[A-Z]/.test(this.formChangePasswd.value.newPasswd!);
  }

  newMdpAllGood(): boolean{
    return this.hasNumber() && this.hasRequiredLenght() && this.hasSpecialCharacter() && this.hasUppercase();
  }

  inputsAllGood(): boolean{
    return this.goodOldPass && this.goodNewPass && this.goodRptNewPass;
  }

  allGood(){
    return this.newMdpAllGood() && this.inputsAllGood() && this.formChangePasswd.valid;
  }

  onClick(){
    if (this.password === 'password') {
      this.password = 'text';
    } else {
      this.password = 'password';
    }
  }
}
