from django.shortcuts import render, redirect
import pickle
import pandas as pd
import bz2

# Helper function for transforming 'type_fire'
def helper(x):
    if x == 0:
        return [0, 0]
    elif x == 2:
        return [1, 0]
    else:
        return [0, 1]

# Placeholder for binning logic
def bin_scan(scan_value):
    # Implement the actual binning logic as required by your model
    return scan_value  # Adjust this return value based on binning logic

def first(request):
    res = 0
    if request.method == 'POST':
        if request.POST.get('pred_button'):
            latitude = float(request.POST.get('lat'))
            longitude = float(request.POST.get('long'))
            bright = float(request.POST.get('bright'))
            daynight = int(request.POST.get('dn'))
            frp = float(request.POST.get('frp'))
            type_fire = int(request.POST.get('type_fire'))
            scan = int(request.POST.get('scan'))
            year = int(request.POST.get('year'))
            month = int(request.POST.get('month'))
            date = int(request.POST.get('date'))
            satellite = request.POST.get('satellite')  # Ensure satellite value is provided

            if -90 <= latitude < 91:  # Simplified the latitude condition
                # Use the exact column names and order from the model training
                feature_names = [
                    'latitude', 'longitude', 'brightness', 'satellite','frp', 'daynight', 
                    'type_2', 'type_3', 'scan_binned', 'year', 'month', 'day'
                ]
                
                # Prepare the data for prediction
                temp = helper(type_fire)
                data = {
                    'latitude': latitude, 'longitude': longitude,
                    'brightness': bright, 'daynight': daynight,
                    'frp': frp, 'type_2': temp[0], 'type_3': temp[1],
                    'scan_binned': bin_scan(scan),  # Implement binning logic if needed
                    'year': year, 'month': month, 'day': date, 'satellite': satellite
                }
                
                # Create DataFrame with the exact feature names and order
                df2 = pd.DataFrame([data], columns=feature_names)

                # Load the model from disk
                with bz2.BZ2File('polls/ForestModel.bz2', 'rb') as file:
                    loaded_model = pickle.load(file)

                # Predict the result using the loaded model
                res = loaded_model.predict(df2)

        else:
            return redirect('homepage')
    else:
        pass

    return render(request, 'index.html', {'result': res})







