#!/bin/bash

export ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export DATA_DIR=${ROOT_DIR}/data
export WORK_DIR=${ROOT_DIR}/work # for temporary files
export OUT_DIR=${ROOT_DIR}/predicted_supersenses # for classifier outputs
export SRC_DIR=${ROOT_DIR}/src

LABELS=${DATA_DIR}/seed.txt
FEATURES=${DATA_DIR}/VSM/eacl14-faruqui-en-svd-de-64.adj.txt

mkdir -p ${WORK_DIR}
mkdir -p ${OUT_DIR}

if [ -a ${FEATURES}.gz ] ; then
  gunzip -f ${FEATURES}.gz
fi 

echo "Extract seed annotations"
${SRC_DIR}/extract_seed.py --seed_dir ${DATA_DIR}/annotations \
    --out_seed_file ${LABELS} 

echo "Split Test and Train"
${SRC_DIR}/split_train_test.py --seed_file ${LABELS} \
    --features ${FEATURES} \
    --out_train ${WORK_DIR}/train_seed.txt \
    --out_test ${WORK_DIR}/test_seed.txt

echo "Expand by WN synonyms and antonyms"
${SRC_DIR}/expand_labeled_data.py --labeled_data ${WORK_DIR}/train_seed.txt \
    --out_file ${WORK_DIR}/expanded.txt --expand 

${SRC_DIR}/build_training_sets.py --in_file ${WORK_DIR}/train_seed.txt \
    --out_feat ${WORK_DIR}/train_seed.feat \
    --out_labels ${WORK_DIR}/train_seed.labels \
    --test_set ${WORK_DIR}/expanded.txt \
    --out_test_feat ${WORK_DIR}/expanded.feat \
    --out_test_labels ${WORK_DIR}/expanded.labels \
    --features ${FEATURES}

echo "Run multi-way classifier. " #Default - Random Forest with 300 trees
${SRC_DIR}/classify.py --train_features ${WORK_DIR}/train_seed.feat \
    --train_labels ${WORK_DIR}/train_seed.labels \
    --test_features ${WORK_DIR}/expanded.feat \
    --test_predicted_labels_out ${WORK_DIR}/expanded.predicted \
    --write_posterior_probabilities 

echo "Selecting best expanded words"
${SRC_DIR}/filter_expanded.py --predictions ${WORK_DIR}/expanded.predicted \
    --orig_seed ${WORK_DIR}/train_seed.txt \
    --out_file ${WORK_DIR}/expanded_seed.txt

echo "Expand by WN synonyms and antonyms"
${SRC_DIR}/expand_labeled_data.py --labeled_data ${WORK_DIR}/expanded_seed.txt \
    --out_file ${WORK_DIR}/expanded.txt --expand 

${SRC_DIR}/build_training_sets.py --in_file ${WORK_DIR}/expanded_seed.txt \
    --out_feat ${WORK_DIR}/train_seed.feat \
    --out_labels ${WORK_DIR}/train_seed.labels \
    --out_test_feat ${WORK_DIR}/vocab.feat \
    --features ${FEATURES} \
    --include_training

echo "Run multi-way classifier" #Default - Random Forest with 300 trees
${SRC_DIR}/classify.py --train_features ${WORK_DIR}/train_seed.feat \
    --train_labels ${WORK_DIR}/train_seed.labels \
    --test_features ${WORK_DIR}/vocab.feat \
    --test_predicted_labels_out ${WORK_DIR}/vocab.predicted \
    --write_posterior_probabilities \

echo "Accuracy-at-k:"
${SRC_DIR}/eval.py --predicted_results ${WORK_DIR}/vocab.predicted \
    --held_out_seed ${WORK_DIR}/test_seed.txt
echo "(Results may vary for different runs)."
echo ""

${SRC_DIR}/soft_voting.py --predicted_results ${WORK_DIR}/vocab.predicted \
    --out_lemma_file ${OUT_DIR}/words.predicted \
    --out_synset_file ${OUT_DIR}/synsets.predicted

echo "See classifier predictions for lemmas at ${OUT_DIR}/words.predicted"
echo "See classifier predictions for synsets at ${OUT_DIR}/synsets.predicted"

