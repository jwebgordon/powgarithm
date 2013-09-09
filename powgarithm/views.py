import requests
import simplejson as json
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.context_processors import csrf
from random import randint

def page_one(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('input_numbers.html', c)

def input_people_things(request):
    c = {}
    c.update(csrf(request))
    num_people = int(request.POST.get('numPeople'))
    num_things = int(request.POST.get('numThings'))
    request.session['num_things'] = num_things
    request.session['num_people'] = num_people
    people_count_list = [n for n in xrange(num_people)]
    things_count_list = [n for n in xrange(num_things)]
    people = {}
    things = {}
    for i in people_count_list:
        people[i] = {}
    for i in things_count_list:
        things[i] = {}
    request.session['people'] = people
    request.session['things'] = things
    c['people'] = people
    c['things'] = things
    return render_to_response('name_people_things.html', c)

def rank_things(request):
    c = {}
    c.update(csrf(request))
    people = request.session['people']
    things = request.session['things']
    if not (len(people) == request.session['num_people'] or len(things) == request.session['num_things']):
        return HttpResponse('SOMETHING WENT TERRIBLY WRONG')
    for index,person in people.iteritems():
        person['name'] = request.POST.get('person'+str(index)+'Name')
    for index,thing in things.iteritems():
        thing['name'] = request.POST.get('thing'+str(index)+'Name')
    c['people'] = people
    c['things'] = things
    request.session['people'] = people
    request.session['things'] = things
    return render_to_response('rank_things.html',c)

def output_results(request):
    people = request.session['people']
    things = request.session['things']
    print things
    winners = []
    for index,thing in things.iteritems():
        rankings = {}
        weights = {}
        total_weight = 0
        for index2,person in people.iteritems():
            rankings[index2] = int(request.POST.get('person'+str(index2)+'Thing'+str(index)))
            weights[index2] = (int(request.session['num_things']) + 1 - int(request.POST.get('person'+str(index2)+'Thing'+str(index))))
            total_weight = total_weight + weights[index2]
        thing['rankings'] = rankings
        thing['weights'] = weights
        thing['total_weight'] = total_weight

    for index, thing in things.iteritems():
        rando_list = []
        for person_no,weight in thing['weights'].iteritems():
            if not person_no in winners:
                for i in range(0,weight):
                    rando_list.append(person_no)
        thing['winner_id'] = rando_list.pop(randint(0,len(rando_list)-1))
        thing['winner'] = people[thing['winner_id']]
        thing['winner_ranking'] = thing['rankings'][thing['winner_id']]
        winners.append(thing['winner_id'])
        print thing
        print rando_list
    for index, thing in things.iteritems():
        potential_swappers = []
        for person_no, rank in thing['rankings'].iteritems():
            if int(rank) < thing['winner_ranking']:
                potential_swappers.append({'id':person_no,'name':people[person_no]['name']})
        thing['potential_swappers'] = potential_swappers

    return render_to_response('output_results.html',{'people':people, 'things':things})
    



    