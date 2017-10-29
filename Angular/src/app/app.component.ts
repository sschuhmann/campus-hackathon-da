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
  id: string;
  start: string;
  destination: string;
  date_time: string;
  visibility = false;
  imagePath: string;


  constructor(private httpClient: HttpClient) {  }

  getValues() {
    const headers = new HttpHeaders().set('Content-Type', 'application/json; charset=utf-8');
    this.httpClient.post('http://192.168.179.43:12000/route',
    {start: this.start, destination: this.destination, date_time: this.date_time},
    {headers: headers})
    .subscribe(data => {
      console.log(data['recommendation']);

      this.imagePath = '/assets/Images/' + data['recommendation'] + '.png';
      this.visibility = true;
    }, (err: HttpErrorResponse) => {
      console.log('Fehler');
    });
  }
}
