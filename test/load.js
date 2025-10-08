import http from 'k6/http';
import {check, sleep} from 'k6';

export const options = {
 stages: [
    { duration: '30s', target: 10 }, // Ramp-up to 100 users over 2 minutes
    { duration: '1m', target: 10 }, // Stay at 100 users for 5 minutes
    { duration: '30s', target: 0 },   // Ramp-down to 0 users over 2 minutes
  ],
};
export default function(){
    const res = http.get('http://localhost:8001/');
    check(res, {
        'status is 200': (r) => r.status === 200,
    });
    sleep(1);
}