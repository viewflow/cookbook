from django.shortcuts import render


def dashboard_view(request):
    return render(request, 'board/dashboard.html', {
        'users_count': 20,
        'graph': {
            "type": "line",
            "data": {
                "labels": ["January", "February", "March", "April", "May", "June", "July"],
                "datasets": [
                    {
                        "data": [65, 59, 80, 81, 56, 55, 40],
                        "fill": False,
                        "borderColor": "rgb(75, 192, 192)",
                        "lineTension": 0.1
                    }
                ]
            },
            "options": {
                'legend': {
                    'display': False
                },
                'animation': {
                    'duration': 0,
                },
            }
        },
        'sales': {
            'type': 'bar',
            'data': {
                'labels': ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
                'datasets': [{
                    'data': [12, 19, 3, 5, 2, 3],
                    'backgroundColor': [
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 206, 86, 0.2)',
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(153, 102, 255, 0.2)',
                        'rgba(255, 159, 64, 0.2)'
                    ],
                    'borderColor': [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)',
                        'rgba(255, 159, 64, 1)'
                    ],
                    'borderWidth': 1
                }]
            },
            'options': {
                'legend': {
                    'display': False
                },
                'animation': {
                    'duration': 0,
                },
                'scales': {
                    'yAxes': [{
                        'ticks': {
                            'beginAtZero': True
                        }
                    }]
                }
            }
        }
    })
