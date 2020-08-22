REALTIME_EVENTING_BACKEND = {      # our
    'ENGINE': 'eventtracking.backends.realtime_eventing.RealtimeEventsBackend',
    'OPTIONS': {
        'processors': [
            {
                'ENGINE': 'eventtracking.filters.routing_filter.RoutingFilter',
                'OPTIONS': {}
            }
        ],
        'backends': {
            'async_realtime_eventing': {
                'ENGINE': 'eventtracking.backends.async_routing.AsyncRoutingBackend',
                'OPTIONS': {
                    # 'whitelist': ['asd','123'],
                    # 'key': 'value',
                    # 'dict':{
                    #     'key':'value'
                    # },
                    'backends': {
                        'caliper': {
                            'ENGINE': 'eventtracking.caliper.backends.CaliperBackend',
                            'OPTIONS': {
                                'processors': [
                                    {'ENGINE': 'track.shim.LegacyFieldMappingProcessor'},
                                    {'ENGINE': 'track.shim.PrefixedEventProcessor'}
                                    #                 {'ENGINE':'translator'},
                                    #                 {'ENGINE':'validator'},
                                    #                 {'ENGINE':'filter'},
                                    #                 {'ENGINE':'router'}
                                ]
                            }
                        },
                        'xAPI': {
                            'ENGINE': 'eventtracking.xAPI.backends.XApiBackend',
                            'OPTIONS': {
                                'processors': [
                                    {'ENGINE': 'track.shim.LegacyFieldMappingProcessor'},
                                    {'ENGINE': 'track.shim.PrefixedEventProcessor'}
                                    #                 {'ENGINE':'translator'},
                                    #                 {'ENGINE':'validator'},
                                    #                 {'ENGINE':'filter'},
                                    #                 {'ENGINE':'router'}
                                ]
                            }
                        }
                    },
                    'processors': []
                }
            }
        }
    }
}

EVENT_TRACKING_BACKENDS = {
    'tracking_logs': {
        '...': {},
        'OPTIONS': {
            'backends': {
                '...': {},
                'realtime_eventing': REALTIME_EVENTING_BACKEND
            }
        }
    },
