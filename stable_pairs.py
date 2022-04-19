# coding: utf-8
"""
@author: Xiangwen Ji
@email: jxw01@pku.edu.cn
@desc: stable marriage algorithm
"""
from collections import defaultdict
from copy import deepcopy


def stable_pairs(requesters, acceptors, similarities):
    # a dictionary to store the similarities of each pair
    sim_dict = {}
    # the list of acceptors in descending order of similarity to each requester
    # requester -> list[acceptors]
    sim_rank = defaultdict(list)
    req_pairs = {}  # pairing result, requester -> acceptor
    acp_pairs = {}  # pairing result, acceptor -> requester
    for req, acp, sim in sorted(
        zip(requesters, acceptors, similarities), key=lambda x: x[2], reverse=True
    ):
        sim_rank[req].append(acp)
        sim_dict[(req, acp)] = sim
        req_pairs[req] = None
        acp_pairs[acp] = None
    # until all requesters already have a pair or have asked all acceptors for a pair:
    # (1) each unpaired requester asks for a pair with the acceptor who has the highest similarity and is not asked before;
    # (2) each acceptor pairs with the highest similar requester and rejects the other requesters.
    while True:
        last_sim_rank = deepcopy(sim_rank)
        for req in sim_rank.keys():
            if req_pairs[req] is not None:
                # requester has a pair, skip
                continue
            if len(sim_rank[req]) == 0:
                # requester has asked all acceptors for a pair, skip
                continue
            # get the next acceptor of this requester
            acp = sim_rank[req].pop(0)
            if acp_pairs[acp] is None:
                # the acceptor does not have a pair, pair temporarily
                acp_pairs[acp] = req
                req_pairs[req] = acp
            else:
                # the acceptor has a pair, compare the similarities
                if sim_dict[(req, acp)] > sim_dict[(acp_pairs[acp], acp)]:
                    # the similarity of the current requester to the acceptor is greater than the similarity of the acceptor to its original pair
                    # the acceptor choose to pair with the current requester
                    req_pairs[acp_pairs[acp]] = None
                    acp_pairs[acp] = req
                    req_pairs[req] = acp
        if last_sim_rank == sim_rank:
            break
    return req_pairs, acp_pairs


if __name__ == "__main__":
    from json import load

    with open("signature_similarity.json", "r", encoding="utf-8") as f:
        sim = load(f)
    req_pairs1, acp_pairs1 = stable_pairs(
        sim["CP-CRC-signature"], sim["ZN-CRC-signature"], sim["cosine-similarity"]
    )
    print(req_pairs1)
    print(acp_pairs1)
    # exchange the requesters and acceptors
    req_pairs2, acp_pairs2 = stable_pairs(
        sim["ZN-CRC-signature"], sim["CP-CRC-signature"], sim["cosine-similarity"]
    )
    print(req_pairs2)
    print(acp_pairs2)
    print(req_pairs1 == acp_pairs2)
    print(acp_pairs1 == req_pairs2)
