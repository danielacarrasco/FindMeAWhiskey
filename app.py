#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 17:33:44 2021

@author: daniela
"""
# -*- coding: utf-8 -
from flask import Flask, render_template, request, redirect, session

import pandas as pd
import numpy as np

import seaborn as sns; sns.set()



df = pd.read_csv('/Data/Reviews_Tags.csv')

sample_data = df[['name', 'price', 'review.point', 'category', 'tags']].reset_index(drop=True)            


app = Flask(__name__, static_folder='static')

app.secret_key = b'_5#y2L"Fdsadsa4Q8zkl\n\xec]/'
#app.config['SESSION_TYPE'] = 'null'
#app.config.from_object(__name__)
#Session(app)

global data

@app.template_filter()
def currencyFormat(value):
    value = float(value)
    return "${:,.2f}".format(value)


@app.route('/', methods=['GET', 'POST'])
def index():
    render_template('index.html')
    if request.method == 'POST':
        session['flavour1'] = request.form['flavour1']
        session['flavour2'] = request.form['flavour2']
        session['flavour3'] = request.form['flavour3']
        session['flavour_exc'] = request.form["flavour_exc"]
        return redirect('/recommendations')
    else:
        return render_template('index.html')

@app.route('/es', methods=['GET', 'POST'])
def index_es():
    render_template('index_es.html')
    if request.method == 'POST':
        session['flavour1'] = request.form['flavour1']
        session['flavour2'] = request.form['flavour2']
        session['flavour3'] = request.form['flavour3']
        session['flavour_exc'] = request.form["flavour_exc"]
        return redirect('/recomendaciones')
    else:
        return render_template('index_es.html')


@app.route('/recommendations', methods=['GET', 'POST'])
def recommendations():
    flavour1 = session['flavour1']
    flavour2 = session['flavour2']
    flavour3 = session['flavour3']
    flavour_exc = session['flavour_exc']
    price = request.values.get('price')
    
    data = df[(df['tags'].astype(str).str.contains(str(flavour1), na=False)) & 
             (df['tags'].astype(str).str.contains(str(flavour2), na=False)) &
             (df['tags'].astype(str).str.contains(str(flavour3), na=False))].reset_index(drop=True)
    data = data[~df['tags'].astype(str).str.contains(str(flavour_exc))].reset_index(drop=True)

    if request.method == 'POST':
        if price=='low':
            data = data[data['price'].astype(float)<100].reset_index(drop=True)
        elif price=='mid':
            data = data[np.logical_and(data['price'].astype(float)>=100,
                        data['price'].astype(float)<200)].reset_index(drop=True)
        elif price=='high':
            data = data[data['price'].astype(float)>=200].reset_index(drop=True)
        
    return render_template('recommendations.html', len = len(data), 
                           whiskeys = data['name'],
                            cat = data['category'],
                            price = data['price'],
                            review = data['review.point'], flavour1 = flavour1, 
                                flavour2 = flavour2, flavour3 = flavour3, flavour_exc = flavour_exc)



@app.route('/recomendaciones', methods=['GET', 'POST'])
def recommendations_es():
    flavour1 = session['flavour1']
    flavour2 = session['flavour2']
    flavour3 = session['flavour3']
    flavour_exc = session['flavour_exc']
    price = request.values.get('price')
    
    data = df[(df['tags'].astype(str).str.contains(str(flavour1), na=False)) & 
             (df['tags'].astype(str).str.contains(str(flavour2), na=False)) &
             (df['tags'].astype(str).str.contains(str(flavour3), na=False))].reset_index(drop=True)
    data = data[~df['tags'].astype(str).str.contains(str(flavour_exc))].reset_index(drop=True)

    if request.method == 'POST':
        if price=='low':
            data = data[data['price'].astype(float)<100].reset_index(drop=True)
        elif price=='mid':
            data = data[np.logical_and(data['price'].astype(float)>=100,
                        data['price'].astype(float)<200)].reset_index(drop=True)
        elif price=='high':
            data = data[data['price'].astype(float)>=200].reset_index(drop=True)
    return render_template('recommendations_es.html', len = len(data), 
                           whiskeys = data['name'],
                            cat = data['category'],
                            price = data['price'],
                            review = data['review.point'], flavour1 = flavour1, 
                                flavour2 = flavour2, flavour3 = flavour3, flavour_exc = flavour_exc)






@app.route('/how-it-works')
def how_it_works():
  return render_template('howitworks.html')

@app.route('/como-funciona')
def how_it_works_es():
  return render_template('howitworks_es.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    return render_template('contact.html')

@app.route('/contacto', methods=['GET', 'POST'])
def contact_es():
    return render_template('contacto.html')



if __name__ == '__main__':
  app.run()
  