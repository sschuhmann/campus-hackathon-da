import { Component } from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {HttpHeaders} from '@angular/common/http';
import {HttpErrorResponse} from '@angular/common/http';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})


export class AppComponent {
  start: string;
  destination: string;
  date_time: string;

  id: string;

  visibility = false;
  visibilityFeedback = false;
  imagePath: string;


  constructor(private httpClient: HttpClient) {  }

  getValues() {
    const headers = new HttpHeaders().set('Content-Type', 'application/json; charset=utf-8');
    this.httpClient.post('http://192.168.179.46:12000/route',
    {start: this.start, destination: this.destination, date_time: this.date_time},
    {headers: headers})
    .subscribe(data => {
      this.id = data['id'];
      this.imagePath = '/assets/Images/' + data['recommendation'] + '.png';
      this.visibility = true;
    }, (err: HttpErrorResponse) => {
      console.log('Fehler');
    });
  }

  sendFeedback(type: string) {
    const headers = new HttpHeaders().set('Content-Type', 'application/json; charset=utf-8');
    this.httpClient.post('http://192.168.179.46:12000/feedback',
    {id: this.id, type: type},
    {headers: headers})
    .subscribe(data => {
      this.visibilityFeedback = true;
    }, (err: HttpErrorResponse) => {
      console.log('Fehler');
    });
  }
}
