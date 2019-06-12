from flask import request, g
import json

# local imports
from server import app
from server.elasticsearch import cards, search
from server.forms import DeckImportForm, SearchForm

from flask import Flask, render_template, flash, redirect, jsonify

@app.route('/')
def under_construction():
    return render_template('base.html')

@app.route('/random')
def random():
    card_info = cards.random_card()
    return json.dumps(card_info, sort_keys=True, indent=4, separators=(',', ': '))

@app.route('/search')
def search_cards():
    output = []
    if request.query_string is not None and request.args.get('q') is not None:
        query_string = request.args.get('q')
        response = search.do_search(query_string)
        for hit in response:
            output.append(hit.to_dict())
    s = SearchForm()
    return render_template('search.html', data=output, form=s)

@app.route('/import', methods=['GET', 'POST'])
def import_deck():
    form = DeckImportForm()
    if form.validate_on_submit():
        text = request.form.get('deck_box')
        # Process the deck, then redirect to it
        decklist = search.find_from_arena_import(text)
        return render_template('deck_view.html', deck=decklist)
        #return redirect('/random')
    # Show form
    return render_template('import_deck.html', title='Import deck from Arena', form=form)