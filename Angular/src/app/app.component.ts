import { Component } from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {HttpHeaders} from '@angular/common/http';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})


export class AppComponent {

  start: string;
  destination: string;
  date_time: string;
  results: string;


  constructor(private httpClient: HttpClient) {

  }

  getValues() {
    const headers = new HttpHeaders().set('Content-Type', 'application/json; charset=utf-8');
    headers.append('Access-Control-Allow-Origin', '*');

    this.httpClient.post('http://192.168.179.43:12000/route', {start: this.start, destination: this.destination, date_time: this.date_time},
    {headers: headers})
    .subscribe(data => {
      this.results = data['results'];
    });
  }
}
