import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})


export class AppComponent {

  start: string;
  destination: string;
  date_time: string;

  getValues() {
    console.log(this.start);
  }
}
