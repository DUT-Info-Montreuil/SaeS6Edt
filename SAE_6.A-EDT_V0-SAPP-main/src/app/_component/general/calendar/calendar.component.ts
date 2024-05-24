import { ChangeDetectorRef, Component, NgZone, OnInit } from '@angular/core';
import { User } from 'src/app/_model/entity/user.model';
import { UserService } from 'src/app/_service/user.service';



@Component({
    selector: 'app-calendar',
    templateUrl: './calendar.component.html',
    styleUrls: ['./calendar.component.scss'],
  })

export class Calendar{

    loading: boolean = false;
    user: User

    constructor(private userService: UserService) { }

    /*
        @function ngOnInit
        @desc: on init
    */
    ngOnInit() {
        this.loading = true
        this.userService.getIdentify().subscribe({
            next: (user: User) => {
                this.user = user
                this.loading = false
            },
            error: (err: any) => {
                console.log(err);
            }
        });
    }
}

