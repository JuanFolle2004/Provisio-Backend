<?php

declare(strict_types=1);

namespace Src\Products\Domain\Model;

use Illuminate\Database\Eloquent\Casts\Attribute;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;
use Illuminate\Database\Eloquent\Relations\HasMany;
use Src\Assignment\Domain\Model\Assignment;
use Src\Groups\Domain\Model\Group;
use Src\Users\Domain\Models\User;

/**
 * @property int                          $id
 * @property string                       $name
 * @property int                          $group_id
 * @property int                          $amount
 * @property \Carbon\CarbonImmutable|null $created_at
 * @property \Carbon\CarbonImmutable|null $updated_at
 * @property-read \Illuminate\Database\Eloquent\Collection<int, Assignment> $assignments
 * @property-read int|null $assignments_count
 * @property-read Group $group
 * @property-read \Illuminate\Database\Eloquent\Collection<int, User> $users
 * @property-read int|null $users_count
 * @property-read bool $is_free
 * @property-read int $remaining_amount
 *
 * @method static \Illuminate\Database\Eloquent\Builder<static>|Product newModelQuery()
 * @method static \Illuminate\Database\Eloquent\Builder<static>|Product newQuery()
 * @method static \Illuminate\Database\Eloquent\Builder<static>|Product query()
 * @method static \Illuminate\Database\Eloquent\Builder<static>|Product whereAmount($value)
 * @method static \Illuminate\Database\Eloquent\Builder<static>|Product whereCreatedAt($value)
 * @method static \Illuminate\Database\Eloquent\Builder<static>|Product whereGroupId($value)
 * @method static \Illuminate\Database\Eloquent\Builder<static>|Product whereId($value)
 * @method static \Illuminate\Database\Eloquent\Builder<static>|Product whereName($value)
 * @method static \Illuminate\Database\Eloquent\Builder<static>|Product whereUpdatedAt($value)
 *
 * @mixin \Eloquent
 */
class Product extends Model
{
    protected $table = 'products';

    protected $guarded = [];

    // @phpstan-ignore-next-line
    protected $appends = ['is_free', 'remaining_amount'];

    /**
     * @return BelongsTo<Group, $this>
     */
    public function group(): BelongsTo
    {
        return $this->belongsTo(Group::class);
    }

    /**
     * @return HasMany<Assignment, $this>
     */
    public function assignments(): HasMany
    {
        return $this->hasMany(Assignment::class);
    }

    /**
     * @return Attribute<bool, never>
     */
    public function isFree(): Attribute
    {
        $assigned = $this->assignments()->sum('amount');

        return Attribute::make(
            get: fn (): bool => $this->amount - $assigned > 0
        );
    }

    /**
     * @return Attribute<int, never>
     */
    public function remainingAmount(): Attribute
    {
        $assigned = $this->assignments()->sum('amount');

        return Attribute::make(
            get: fn (): int|float => $this->amount - $assigned
        );
    }

    /**
     * @return BelongsToMany<User, $this>
     */
    public function users(): BelongsToMany
    {
        return $this->belongsToMany(User::class, 'assignment');
    }
}
