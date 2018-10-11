def first_entity_value(entities, entity):
        if entity not in entities:
            return None
        val = entities[entity][0]['value']
        if not val:
            return None
        return val

def manage_request(request):
    #All current keywords and commands
    entities = request['entities']
    greetings = first_entity_value(entities, 'greetings')
    search = first_entity_value(entities, 'search')
    ban = first_entity_value(entities, 'ban')
    kick = first_entity_value(entities, 'kick')
    openB = first_entity_value(entities, 'open')
    say = first_entity_value(entities, 'say')

    if search:
        search_query = first_entity_value(entities, 'search_query')
        number_of_results = first_entity_value(entities, 'number_of_results')
        if search_query:
            number = 5
            if number_of_results:
                number = int(number_of_results)
            return "search", search_query, number
        else:
            return "error"
                
    elif ban:
        player = first_entity_value(entities, 'player')
        if player:
            return "ban", player
        else:
            return "error"

    elif kick:
        player = first_entity_value(entities, 'player')
        if player:
            return "kick", player
        else:
            return "error"

    elif openB:
        if(first_entity_value(entities, 'terminal')):
            return "open", "terminal"

    elif say:
        message = first_entity_value(entities, '')
        if message:
            channel = first_entity_value(entities, 'location')
            if channel:
                return "say", message, channel
            return "say", message
        else:
            return "error"
        
    elif greetings:
        return "greetings"
    
    else:
        return "error"
        
if __name__ == '__main__':
    pass
