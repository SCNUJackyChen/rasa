#!/bin/bash                                            
rasa run actions &
rasa run --enable-api --cors "*"