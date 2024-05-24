import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { ToastrService } from 'ngx-toastr';
import { WeekCommentService } from 'src/app/_service/weekComment.service';
import { WeekComment } from 'src/app/_model/entity/weekComment.model';
import { Promotion } from 'src/app/_model/entity/promotion.model';

@Component({
  selector: 'comment-add',
  templateUrl: './comment-add.component.html',
  styleUrls: ['./comment-add.component.scss']
})
export class CommentAddComponent implements OnInit {
  commentForm: FormGroup;
  @Input() comment?: WeekComment;
  @Input() date: Date;
  @Input() weekNumber: number;
  @Input() promo: Promotion;
  @Output() updateOrCreate: EventEmitter<WeekComment> = new EventEmitter<WeekComment>();
  @Output() remove: EventEmitter<WeekComment> = new EventEmitter<WeekComment>();
  @Output() closeModal: EventEmitter<void> = new EventEmitter<void>();

  constructor(
    private formBuilder: FormBuilder,
    private commentService: WeekCommentService,
    private toastr: ToastrService
  ) {}

    
  /*
      @function ngOnInit
      @desc: on init form
  */
  ngOnInit() {
    if (!this.comment){
      this.comment = new WeekComment();
    }

    this.commentForm = this.formBuilder.group({
      content: [this.comment.content, [
      ]],
    });
  }
    
  /*
      @function onSubmit
      @desc: on submit form send comment
  */
  onSubmit() {
    if (this.commentForm.invalid) {
      return;
    }
    const comment_value: WeekComment = this.commentForm.value;
    comment_value.year = this.date.getFullYear().toString();
    comment_value.week_number = this.weekNumber;
    comment_value.id_promo = this.promo.id;

    this.commentService.addComment(comment_value).subscribe({
      next: comment => {
        if (comment_value.content != "") this.updateOrCreate.emit(comment);
        else {
          this.remove.emit(comment);
        }
        this.closeModalAdd();
      },
      error: response => {
        console.log(response);
        this.toastr.error(response.error.error, 'Erreur', { timeOut: 2000 });
      },
    });
  }
  /*
    @function closeModalAdd
    @desc: close modal emit to parent
  */
  closeModalAdd() {
    this.closeModal.emit();
  }
}