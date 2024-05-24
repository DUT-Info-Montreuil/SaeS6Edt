import { Injectable } from '@angular/core';
import { Subject, Subscription } from 'rxjs';
import { filter, map } from 'rxjs/operators';
import { EventData } from './event.class';

@Injectable({
  providedIn: 'root',
})
export class EventBusService {
  private subject$ = new Subject<EventData>();


  /*
      @function emit
      @param event: EventData
      @desc: emit event
  */
  emit(event: EventData) {
    this.subject$.next(event);
  }

  /*
      @function on
      @param eventName: string
      @param action: any
      @return Subscription
      @desc: on event
  */
  on(eventName: string, action: any): Subscription {
    return this.subject$.pipe(
      filter((e: EventData) => e.name === eventName),
      map((e: EventData) => e["value"])).subscribe(action);
  }
}
