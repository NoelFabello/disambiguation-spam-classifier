import { Component, OnInit } from '@angular/core';
import { ApiService } from './python-api.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit{

  title = 'disambiguationApp';

  constructor(private readonly apiService: ApiService, private readonly router: Router) { }

  ngOnInit(): void {
    window.addEventListener('pywebviewready', () => {
      this.apiService.setApi(true, window.pywebview.api);
    })
  }

  isActive(route: string): boolean {
    return this.router.url.includes(route);
  }

  Close() {
    this.apiService.Close()
  }
}
