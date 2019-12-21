<?xml version="1.0" encoding="UTF-8"?>
<config xmlns="http://www.knime.org/2008/09/XMLConfig" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.knime.org/2008/09/XMLConfig http://www.knime.org/XMLConfig_2008_09.xsd" key="dialog">
<config key="internal_node_subsettings">
<entry key="memory_policy" type="xstring" value="CacheSmallInMemory"/>
</config>
<config key="model">
<entry key="sourceCode" type="xstring" value="import numpy as np%%00010import scipy.spatial.distance as dist%%00010import scipy.stats%%00010import operator%%00010%%00010#temos 15 utilizadores aqui, não sei porque%%00010#vou separar cada utilizador com os seus ratings%%00010def ratings_of_users(ratings,user_max):%%00010%%00010%%00009ratings_users = {}%%00010%%00010%%00009for i in range(1,user_max):%%00010%%00009%%00009tmp = []%%00010%%00009%%00009ratings_users[&quot;user_&quot;+str(i)] = []%%00010%%00010%%00009for row in ratings:%%00010%%00009%%00009id = np.int(row[0])%%00010%%00009%%00009ratings_users[&quot;user_&quot;+str(id)].append((row[3],row[1]));%%00010%%00009%%00009%%00010%%00009return ratings_users;%%00010%%00010def best_matches(ratings,user):%%00010%%00009%%00010%%00009specific_ratings_user = ratings[user]%%00010%%00009ratings.__delitem__(user)%%00010%%00010%%00009#todos os filmes referentes ao user a prever%%00010%%00009x = len(specific_ratings_user)%%00010%%00009movies_user = np.empty((1,x),np.int)%%00010%%00009i=0;%%00010%%00009for tuplo in specific_ratings_user:%%00010%%00009%%00009movies_user[0][i] = tuplo[1]%%00010%%00009%%00009i = i+1;%%00010%%00010%%00009#agora preciso de todos os movies e ratings dos outros utilizadores%%00010%%00009#que avaliaram os mesmos movies que o user especifico%%00010%%00009ratings_users = {}%%00010%%00010%%00009for i in ratings:%%00010%%00009%%00009tmp = []%%00010%%00009%%00009ratings_users[i] = []%%00010%%00009%%00009%%00010%%00009for row in ratings:%%00010%%00009%%00009%%00010%%00009%%00009for tuplo in ratings[row]:%%00010%%00009%%00009%%00009movie = tuplo[1]%%00009%%00010%%00009%%00009%%00009%%00010%%00009%%00009%%00009if (movie in movies_user[0]):%%00010%%00009%%00009%%00009%%00009ratings_users[row].append((tuplo[0],tuplo[1]))%%00010%%00010%%00009return specific_ratings_user,ratings_users%%00010%%00010#dá uma lista com as similaridades entre utilizadores%%00010#vou ao utilizador que quero prever e para cada outro utilizador%%00010#encontro filmes que ambos avaliaram e calculo a similaridade%%00010def similaridade(user, group_of_users):%%00010%%00010%%00009#users%%00010%%00009ratings_similar = {}%%00010%%00009similarity_user = []%%00010%%00009similarity_between_users = []%%00010%%00009%%00010%%00009#specific user%%00010%%00009ratings_similar[&quot;user&quot;] = [];%%00010%%00009movies_user = []%%00010%%00009%%00010%%00009#para cada utilizador%%00010%%00009for x in group_of_users:%%00010%%00010%%00009%%00009#percorremos os filmes%%00010%%00009%%00009for tuplo in group_of_users[x]:%%00010%%00009%%00009%%00009#só quero os filmes que o user1 avaliou%%00009semelhantes ao user2%%00009%%00010%%00009%%00009%%00009for movie in user:%%00010%%00009%%00009%%00009%%00009if(movie[1]==tuplo[1]):%%00010%%00009%%00009%%00009%%00009%%00009ratings_similar[&quot;user&quot;].append(movie[0])%%00010%%00009%%00009%%00010%%00009%%00009#print(&quot;user to predict = &quot; + str(ratings_similar[&quot;user&quot;]))%%00010%%00009%%00009#print(&quot;user to compare = &quot; + str(group_of_users[x]));%%00010%%00009%%00009tmp = []%%00010%%00009%%00009for i in group_of_users[x]:%%00010%%00009%%00009%%00009tmp.append(i[0])%%00010%%00010%%00009%%00009group_of_users[x] = tmp%%00010%%00010%%00009%%00009#print(&quot;user to predict = &quot; + str(ratings_similar[&quot;user&quot;]))%%00010%%00009%%00009#print(&quot;user to compare = &quot; + str(group_of_users[x]));%%00010%%00009%%00009%%00010%%00009%%00009#calcular a similaridade com a euclidian distance%%00010%%00009%%00009if( ratings_similar[&quot;user&quot;] != [] and  group_of_users[x] != []):%%00010%%00009%%00009%%00009%%00010%%00009%%00009%%00009tmp1 = ratings_similar[&quot;user&quot;]%%00010%%00009%%00009%%00009tmp2 = group_of_users[x]%%00010%%00009%%00009%%00009if(len(tmp1) &gt; 1 and len(tmp2) &gt; 2):%%00010%%00009%%00009%%00009%%00009tmp = scipy.stats.pearsonr(tmp1,tmp2)%%00010%%00009%%00009%%00009%%00009similarity_between_users.append(tmp)%%00010%%00009%%00009%%00009%%00009similarity_user.append(x)%%00010%%00009%%00009%%00009%%00010%%00009%%00009ratings_similar[&quot;user&quot;] = [];%%00010%%00010%%00010%%00009return np.asarray(similarity_between_users[0]), np.asarray(similarity_user);%%00010%%00009%%00009%%00010%%00010def TopN(similarity_between_users, N):%%00010%%00009i = 0%%00010%%00010%%00009while( N &gt; similarity_between_users.shape[0]):%%00010%%00009%%00009N = N-2;%%00010%%00009%%00009%%00010%%00009#ratings = np.dot(similarity_between_users,-1)%%00010%%00009%%00009%%00010%%00009ind = np.argpartition(similarity_between_users, -N)[-N:]%%00010%%00009return ind;%%00010%%00009%%00010%%00009%%00009%%00010def search_unranked_films(user_to_predict, topN_users,ratings_users,ratings_user_to_predict):%%00010%%00010%%00009list = [];%%00010%%00009movie_list = {};%%00010%%00009users = {}%%00010%%00009for user in topN_users:%%00010%%00009%%00009users[user] = ratings_users[user];%%00010%%00010%%00009x = np.asarray(users)%%00010%%00009%%00010%%00009for user in users:%%00010%%00009%%00009for movie in users[user]:%%00010%%00009%%00009%%00009#verificar se o user1 não viu%%00010%%00009%%00009%%00009#o list serve para não estar a repetir%%00010%%00009%%00009%%00009if(not movie[1] in list):%%00010%%00009%%00009%%00009%%00009tmp = 0; %%00010%%00009%%00009%%00009%%00009for i in ratings_user_to_predict:%%00010%%00009%%00009%%00009%%00009%%00009if(i[1] == movie[1]): %%00010%%00009%%00009%%00009%%00009%%00009%%00009tmp=1;%%00010%%00010%%00009%%00009%%00009%%00009# se chegar aqui e tmp = 0, user não viu/avaliou este filme, posso continuar com este filme%%00010%%00009%%00009%%00009%%00009if(tmp==0):%%00010%%00009%%00009%%00009%%00009%%00009list.append(movie[1]);%%00010%%00009%%00009%%00009%%00009how_many = 1; #esta variável permite me identificar quantos utilizadores viram este filme%%00010%%00009%%00009%%00009%%00009for u in users:%%00010%%00009%%00009%%00009%%00009%%00009if(not u == user):%%00010%%00009%%00009%%00009%%00009%%00009%%00009for m in users[u]:%%00010%%00009%%00009%%00009%%00009%%00009%%00009%%00009if(m[1] == movie[1]):%%00010%%00009%%00009%%00009%%00009%%00009%%00009%%00009%%00009how_many = how_many +1;%%00010%%00009%%00009%%00009%%00009movie_list[movie[1]] = how_many;%%00010%%00009%%00009%%00009%%00009%%00009%%00009%%00010%%00009return movie_list%%00010%%00009%%00009%%00009%%00009%%00009%%00009%%00009%%00010%%00009%%00009%%00009%%00010def predict_movies(user_rating,similarity_users,ratings_user,movies):%%00010%%00009#media de avaliação do user a prever -&gt; ratings_specific_user%%00010%%00009#similaridades entre users -&gt;similarity_be..%%00010%%00009#avaliações individuais -&gt; ratings_users%%00010%%00009#media das avaliacoes -&gt; rratings_user%%00010%%00009#similaridade entre users -&gt; similarity_be%%00010%%00009predict_movie_rating = {};%%00010%%00009user_rating = np.asarray(user_rating)%%00010%%00009ra = np.mean(user_rating[:,0])%%00010%%00009%%00010%%00009numerador = []%%00010%%00009denominador = []%%00010%%00010%%00009#denominador%%00010%%00009for i in similarity_users:%%00010%%00009%%00009denominador.append(i[1])%%00010%%00009%%00010%%00009denominador = np.mean(denominador);%%00010%%00009%%00010%%00009#numerador%%00010%%00009for movie in movies:%%00010%%00009%%00009numbers_of_users_that_rate = movies[movie];%%00010%%00010%%00009%%00009for i in similarity:%%00010%%00009%%00009%%00009%%00010%%00009%%00009%%00009sim_a_b = i[1]#similaridade entre 0 e 1%%00010%%00009%%00009%%00009b = i[0] #nome do utilizador%%00010%%00009%%00009%%00009b = ratings_user[b];%%00010%%00009%%00009%%00009b = np.asarray(b)%%00010%%00009%%00009%%00009rb = np.mean(b[:,0])%%00010%%00009%%00009%%00010%%00009%%00009%%00009#rb_p rating do user x ao filme p%%00010%%00009%%00009%%00009for i in b:%%00010%%00009%%00009%%00009%%00009if(i[1] == movie):%%00010%%00009%%00009%%00009%%00009%%00009rb_p = i[0];%%00010%%00009%%00009%%00009%%00009%%00009%%00010%%00009%%00009%%00009tmp = sim_a_b * (rb_p - rb);%%00010%%00009%%00009%%00009numerador.append(tmp)%%00010%%00010%%00009%%00009#calculo do numerador%%00010%%00009%%00009numerador = np.mean(numerador)%%00010%%00009%%00009tmp = ra + (numerador / denominador)%%00010%%00009%%00009numerador = []%%00010%%00009%%00009%%00010%%00009%%00009predict_movie_rating[movie] = tmp;%%00010%%00009%%00009%%00010%%00009return predict_movie_rating;%%00010%%00009%%00010%%00009%%00010ratings = input_table.copy().to_numpy()%%00010user_to_predict = &quot;user_1&quot;%%00010%%00010#ratings dos utilizadores%%00010ratings_users = ratings_of_users(ratings,16)%%00010%%00010#ratings de um utilizador e dos utilizadores que avalariam filmes semelhantes%%00010ratings_specific_user,ratings_users2 = best_matches(ratings_users,user_to_predict)%%00010%%00010#similaridade entre um utilizador e os calculados em cima%%00010similarity_between_users, similarity = similaridade(ratings_specific_user,ratings_users2);%%00010%%00010#verifica qual os melhores utilizadores(similaridade mais forte)%%00010indx = TopN(similarity_between_users,2);%%00010topN_users = similarity[indx]%%00010%%00010#verifica quais os filmes que os utilizadores mais similares avaliaram, em que o 1 ainda não viu/avaliou%%00010movie_list = search_unranked_films(user_to_predict, topN_users,ratings_users,ratings_specific_user)%%00010%%00010%%00010#similaridade entre users e user em lista%%00010similarity = [];%%00010for i in range(0,len(topN_users)):%%00010%%00009similarity.append((topN_users[i],similarity_between_users[i]))%%00010%%00010#faz o predict da avaliação que o utilizar deverá dar a estes filmes com base em tudo calculado anteriormente%%00010predict_movie_rating = predict_movies(ratings_specific_user,similarity,ratings_users,movie_list)%%00010%%00010#vão todas de 0 a 5, porque estou a usar Pearson Correlation%%00010high_prediction = max(predict_movie_rating.items(), key=operator.itemgetter(1))[1];"/>
<entry key="rowLimit" type="xint" value="1000"/>
<entry key="pythonVersionOption" type="xstring" value="python3"/>
<entry key="python2Command" type="xstring" value=""/>
<entry key="python3Command" type="xstring" value=""/>
<entry key="chunkSize" type="xint" value="500000"/>
<entry key="convertMissingToPython" type="xboolean" value="false"/>
<entry key="convertMissingFromPython" type="xboolean" value="false"/>
<entry key="sentinelOption" type="xstring" value="MIN_VAL"/>
<entry key="sentinelValue" type="xint" value="0"/>
</config>
</config>