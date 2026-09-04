hombre(edgar).
hombre(enrique).
hombre(juan).
hombre(jose).
hombre(mario).
hombre(pablo).
hombre(carlos).
hombre(roberto).
hombre(alberto).
hombre(casimiro).

mujer(luisa).
mujer(berta).
mujer(aide).
mujer(guillermina).
mujer(hilda).
mujer(isabel).
mujer(laura).
mujer(clemencia).

es_hijo_de(edgar,jose).
es_hijo_de(edgar,guillermina).
es_hijo_de(mario,jose).
es_hijo_de(carlos,mario).
es_hijo_de(enrique,edgar).
es_hijo_de(enrique,aide).
es_hijo_de(pablo,edgar).
es_hijo_de(pablo,aide).
es_hijo_de(alberto,roberto).
es_hijo_de(alberto,berta).

es_hija_de(hilda, aide).
es_hija_de(berta, luisa).
es_hija_de(aide, luisa).
es_hija_de(aide, juan).
es_hija_de(isabel, casimiro).
es_hija_de(isabel, berta).
es_hija_de(clemencia, casimiro).
es_hija_de(clemencia, laura).


es_padre_de(P, H):-
    hombre(P),
    es_hijo_de(H, P).

es_padre_de(P, H):-
    hombre(P),
    es_hija_de(H, P).

es_madre_de(M, H):-
    mujer(M), 
    es_hijo_de(H, M).

es_madre_de(M ,H):-
    mujer(M),
    es_hija_de(H, M).

es_hermano_de(H, X):-
    hombre(H),
    es_padre_de(P, H),
    es_padre_de(P, X).

es_hermano_de(H, X):-
    hombre(H),
    es_madre_de(M, H),
    es_madre_de(M, X).

es_hermana_de(H, X):-
    mujer(H),
    es_padre_de(P, H),
    es_padre_de(P, X).

es_hermana_de(H, X):-
    mujer(H),
    es_madre_de(M, H),
    es_madre_de(M, X).

es_ancestro_de(A, D):-
    es_hijo_de(D, A).

es_ancestro_de(A, D):-
    es_hija_de(D, A).

es_ancestro_de(A, D):-
    es_hijo_de(D, P),
    es_ancestro_de(A, P).

es_ancestro_de(A, D):-
    es_hija_de(D, P),
    es_ancestro_de(A, P).

es_abuelo_de(A, C) :-
    hombre(A),
    es_padre_de(A, B),
    (es_padre_de(B, C) ; es_madre_de(B,C)). 

es_abuela_de(A, C) :-
    mujer(A),
    es_madre_de(A, B),
    (es_madre_de(B, C) ; es_padre_de(B, C)).


es_tio_de(T, S):-
    hombre(T),
    (es_hijo_de(S, P); es_hija_de(S, P)),
    (es_hermano_de(P, T); es_hermana_de(P, T)).

es_tia_de(T, S):-
    mujer(T),
    (es_hijo_de(S, P); es_hija_de(S, P)),
    (es_hermano_de(P, T); es_hermana_de(P, T)).

es_sobrino_de(A,C) :-
    hombre(A),
    (es_hermano_de(A,B) ; es_hermana_de(A,B)),
    es_hijo_de(B, C).

es_sobrina_de(A,C) :-
    mujer(A),
    (es_hermano_de(A,B) ; es_hermana_de(A,B)),
    es_hija_de(B, C).


es_primo_de(P, P2):-
    hombre(P),
    (es_tio_de(T, P);es_tia_de(T, P)),
    (es_padre_de(T, P2);es_madre_de(T, P2)).
    
es_prima_de(P, P2):-
    mujer(P),
    (es_tio_de(T, P);es_tia_de(T, P)),
    (es_padre_de(T, P2);es_madre_de(T, P2)).    