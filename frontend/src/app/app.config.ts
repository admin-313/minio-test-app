import { ApplicationConfig, provideZoneChangeDetection } from '@angular/core';
import { provideRouter } from '@angular/router';

import { routes } from './app.routes';
import { provideHttpClient } from '@angular/common/http';

// The method of HTTP calls was discovered here: https://angular.dev/guide/http/setup
export const appConfig: ApplicationConfig = {
  providers: [
    provideZoneChangeDetection({ eventCoalescing: true }),
    provideRouter(routes),
    // To cover interceptors topic read https://angular.dev/guide/http/interceptors#intercepting-response-events
    provideHttpClient(),
  ]
};
