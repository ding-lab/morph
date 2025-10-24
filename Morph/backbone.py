import Morph.modules

def backbone(data, mapper, counter, muxer, morphological_filter, thresholder, algebraic_filter, labeler):
    data = getattr(Morph.modules.Mapper(), mapper[0])(data, *(mapper[1:]))
    data = getattr(Morph.modules.Counter(), counter[0])(data, *(counter[1:]))
    data = getattr(Morph.modules.Muxer(), muxer[0])(data, *(muxer[1:]))
    data = getattr(Morph.modules.MorphologicalFilter(), morphological_filter[0])(data, *(morphological_filter[1:]))
    data = getattr(Morph.modules.Thresholder(), thresholder[0])(data, *(thresholder[1:]))
    data = getattr(Morph.modules.AlgebraicFilter(), algebraic_filter[0])(data, *(algebraic_filter[1:]))
    return getattr(Morph.modules.Labeler(), labeler[0])(data, *(labeler[1:]))
