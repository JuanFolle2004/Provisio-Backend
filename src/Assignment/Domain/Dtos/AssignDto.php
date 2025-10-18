<?php

declare(strict_types=1);

namespace Src\Assignment\Domain\Dtos;

class AssignDto
{
    public function __construct(
        public readonly int $productId,
        public readonly int $groupId,
        public readonly int $amount,
        public readonly int $bought,
    ) {
    }
}
